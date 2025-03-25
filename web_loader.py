from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def load_urls(urls: List[str]):
    """
    Load and process content from a list of URLs using WebBaseLoader.
    
    Args:
        urls (List[str]): List of URLs to load
        
    Returns:
        documents: List of loaded documents
    """
    # Initialize the WebBaseLoader with the URLs
    loader = WebBaseLoader(urls)
    
    try:
        # Load the documents
        documents = loader.load()
        print(f"Successfully loaded {len(documents)} documents")
        return documents
    except Exception as e:
        print(f"Error loading documents: {str(e)}")
        return None

def combine_documents_to_string(documents) -> str:
    """
    Combine all documents into a single string.
    
    Args:
        documents: List of documents to combine
        
    Returns:
        str: Combined text from all documents
    """
    if not documents:
        return ""
    
    # Combine all document contents with double newlines between them
    combined_text = "\n\n".join(doc.page_content for doc in documents)
    print(f"Combined {len(documents)} documents into a single string")
    return combined_text

def load_and_combine_urls(urls: List[str]) -> str:
    """
    Load URLs and combine all documents into a single string.
    
    Args:
        urls (List[str]): List of URLs to load
        
    Returns:
        str: Combined text from all documents
    """
    documents = load_urls(urls)
    if not documents:
        return ""
    return combine_documents_to_string(documents)

def load_and_split_urls(urls: List[str], chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Load URLs and split the content into smaller chunks using RecursiveCharacterTextSplitter.
    
    Args:
        urls (List[str]): List of URLs to load
        chunk_size (int): The size of each text chunk
        chunk_overlap (int): The number of characters to overlap between chunks
        
    Returns:
        splits: List of split documents with enhanced metadata
    """
    # First load the documents
    documents = load_urls(urls)
    if not documents:
        return None
    
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Split the documents
    splits = text_splitter.split_documents(documents)
    
    # Add enhanced metadata to each split
    for i, split in enumerate(splits):
        # Get the source URL from the original document
        source_url = split.metadata.get('source', 'Unknown')
        
        # Add additional metadata
        split.metadata.update({
            'chunk_index': i,
            'total_chunks': len(splits),
            'chunk_size': len(split.page_content),
            'source_url': source_url,
            'chunk_type': 'text'
        })
    
    print(f"Split documents into {len(splits)} chunks")
    return splits

# Example usage
if __name__ == "__main__":
    # Example URLs to load
    sample_urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]
    
    # Load and split the documents
    splits = load_and_split_urls(sample_urls)
    
    # Print preview of each split with metadata
    if splits:
        for i, split in enumerate(splits):
            print(f"\nSplit {i+1} preview:")
            print(f"Source URL: {split.metadata['source_url']}")
            print(f"Chunk {split.metadata['chunk_index'] + 1} of {split.metadata['total_chunks']}")
            print(f"Chunk size: {split.metadata['chunk_size']} characters")
            print("Content preview:")
            print(split.page_content[:200] + "...") 