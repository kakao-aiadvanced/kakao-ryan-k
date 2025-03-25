from web_loader import load_urls, load_and_split_urls, load_and_combine_urls

# Example 1: Loading and splitting a single URL
single_url = ["https://lilianweng.github.io/posts/2023-06-23-agent/"]
splits = load_and_split_urls(single_url, chunk_size=1000, chunk_overlap=200)

if splits:
    print("\nSingle URL Example with Splitting:")
    print(f"Total number of chunks: {len(splits)}")
    for split in splits:
        print(f"\nChunk {split.metadata['chunk_index'] + 1} of {split.metadata['total_chunks']}")
        print(f"Source: {split.metadata['source_url']}")
        print(f"Size: {split.metadata['chunk_size']} characters")
        print("Preview:")
        print(split.page_content[:200] + "...")

# Example 2: Loading and splitting multiple URLs
multiple_urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/"
]

splits = load_and_split_urls(multiple_urls, chunk_size=1000, chunk_overlap=200)

if splits:
    print("\nMultiple URLs Example with Splitting:")
    print(f"Total number of chunks: {len(splits)}")
    
    # Group chunks by source URL
    chunks_by_source = {}
    for split in splits:
        source_url = split.metadata['source_url']
        if source_url not in chunks_by_source:
            chunks_by_source[source_url] = []
        chunks_by_source[source_url].append(split)
    
    # Print chunks grouped by source
    for source_url, chunks in chunks_by_source.items():
        print(f"\nChunks from {source_url}:")
        print(f"Number of chunks: {len(chunks)}")
        for chunk in chunks:
            print(f"\nChunk {chunk.metadata['chunk_index'] + 1} of {chunk.metadata['total_chunks']}")
            print(f"Size: {chunk.metadata['chunk_size']} characters")
            print("Preview:")
            print(chunk.page_content[:200] + "...") 