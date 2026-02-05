import asyncio
import aiohttp
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from model.config import (
    TMDB_API_KEY, 
    TMDB_BASE_URL, 
    TARGET_MOVIE_IDS, 
    RAW_DATA_PATH,
    INGESTION_CONCURRENCY,
    INGESTION_BATCH_SIZE
)
from model.logger import get_logger

logger = get_logger(__name__)

class TMDBClient:
    def __init__(self, api_key: str, base_url: str, semaphore: asyncio.Semaphore):
        self.api_key = api_key
        self.base_url = base_url
        self.semaphore = semaphore
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch(self, url: str, attempt: int = 1, max_retries: int = 5) -> Optional[Dict[str, Any]]:
        """Generic async fetch with exponential backoff and retry limit."""
        params = {"api_key": self.api_key}
        try:
            # Enforce rate/concurrency limit at the Request level
            async with self.semaphore:
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        if attempt > max_retries:
                            logger.error(f"Max retries ({max_retries}) reached for {url}")
                            return None
                            
                        sleep_time = 2 ** attempt  # Exponential backoff: 2s, 4s, 8s...
                        logger.warning(f"Rate limited (429) for {url}. Retrying in {sleep_time}s (Attempt {attempt}/{max_retries})")
                        await asyncio.sleep(sleep_time)
                        
                        # Recursive retry with incremented attempt
                        return await self.fetch(url, attempt + 1, max_retries)
                    elif response.status == 404:
                        logger.warning(f"Resource not found (404) for {url}. Skipping (Permanent Failure).")
                        return None
                    else:
                        logger.error(f"Error {response.status} fetching {url}")
                        return None
        except Exception as e:
            logger.error(f"Request exception for {url}: {e}")
            return None

async def process_movie(client: TMDBClient, movie_id: int) -> Optional[Dict[str, Any]]:
    """Fetches details and credits for a single movie concurrently."""
    
    # Create tasks for both endpoints
    details_url = f"{client.base_url}/movie/{movie_id}"
    credits_url = f"{client.base_url}/movie/{movie_id}/credits"
    
    # Run fetch operations concurrently (semaphore handled inside fetch)
    details_task = client.fetch(details_url)
    credits_task = client.fetch(credits_url)
    
    details, credits = await asyncio.gather(details_task, credits_task)
    
    if details:
        if credits:
            details['credits'] = credits
        return details
    return None

async def run_async_ingestion():
    """Main async orchestration."""
    if not TMDB_API_KEY:
        logger.error("TMDB_API_KEY is missing.")
        return

    start_time = time.time()
    
    # Deduplicate IDs to ensure no duplicate requests
    unique_movie_ids = list(set(TARGET_MOVIE_IDS))
    if len(unique_movie_ids) < len(TARGET_MOVIE_IDS):
        logger.warning(f"Found {len(TARGET_MOVIE_IDS) - len(unique_movie_ids)} duplicate IDs in target list. Deduplicating.")
    
    logger.info(f"Starting Async Ingestion for {len(unique_movie_ids)} unique movies.")
    
    batch_buffer = []
    total_processed = 0
    batch_count = 1
    
    # 1. Initialize Semaphore
    semaphore = asyncio.Semaphore(INGESTION_CONCURRENCY)

    # 2. Pass semaphore to client
    async with TMDBClient(TMDB_API_KEY, TMDB_BASE_URL, semaphore) as client:
        
        # STREAMING: Process IDs in chunks to avoid creating millions of coroutines at once
        # This keeps memory usage low regardless of total movie count
        TASK_CHUNK_SIZE = 1000 
        
        for i in range(0, len(unique_movie_ids), TASK_CHUNK_SIZE):
            chunk_ids = unique_movie_ids[i : i + TASK_CHUNK_SIZE]
            logger.info(f"Processing chunk {i//TASK_CHUNK_SIZE + 1} with {len(chunk_ids)} movies...")
            
            # Create tasks only for this chunk
            tasks = [process_movie(client, mid) for mid in chunk_ids]
            
            # Process this chunk completely before moving to next (or could use more complex sliding window)
            # as_completed yields results as they finish within this chunk
            for task in asyncio.as_completed(tasks):
                data = await task
                if data:
                    batch_buffer.append(data)
                    
                    # Check batch size (independent of chunk size)
                    if len(batch_buffer) >= INGESTION_BATCH_SIZE:
                        save_batch(batch_buffer, batch_count)
                        total_processed += len(batch_buffer)
                        batch_buffer = []
                        batch_count += 1
    
    # Flush remaining
    if batch_buffer:
        save_batch(batch_buffer, batch_count)
        total_processed += len(batch_buffer)

    duration = time.time() - start_time
    logger.info(f"Ingestion Finished. Processed {total_processed} movies in {duration:.2f} seconds.")

def save_batch(buffer: List[Dict], batch_num: int):
    """Saves a list of movie objects as newline-delimited JSON."""
    if not buffer:
        return
        
    filename = f"batch_{batch_num}.json"
    file_path = RAW_DATA_PATH / filename
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for item in buffer:
                f.write(json.dumps(item) + "\n")
        logger.info(f"Saved batch {batch_num} with {len(buffer)} movies to {file_path}")
    except IOError as e:
        logger.error(f"Failed to save batch {batch_num}: {e}")

if __name__ == "__main__":
    # Windows Selector workaround for Python 3.13+ asyncio policies
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(run_async_ingestion())
