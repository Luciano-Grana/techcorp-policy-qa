"""
Document processing module for ingesting and chunking policy documents.
"""

import os
import re
from pathlib import Path
from typing import List, Dict
import hashlib

# Document parsing
import markdown
from bs4 import BeautifulSoup
from pypdf import PdfReader


class Document:
    """Represents a document chunk with metadata."""

    def __init__(self, content: str, metadata: Dict[str, str]):
        self.content = content
        self.metadata = metadata
        self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique ID for chunk based on content and metadata."""
        hash_input = f"{self.metadata.get('source', '')}:{self.content[:100]}"
        return hashlib.md5(hash_input.encode()).hexdigest()


class DocumentProcessor:
    """Handles document parsing, cleaning, and chunking."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize document processor.

        Args:
            chunk_size: Target size of chunks in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_documents(self, directory: str) -> List[Document]:
        """
        Load all documents from a directory.

        Args:
            directory: Path to directory containing documents

        Returns:
            List of Document objects
        """
        documents = []
        directory_path = Path(directory)

        for file_path in directory_path.rglob('*'):
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() == '.md':
                        docs = self._load_markdown(file_path)
                    elif file_path.suffix.lower() == '.pdf':
                        docs = self._load_pdf(file_path)
                    elif file_path.suffix.lower() in ['.html', '.htm']:
                        docs = self._load_html(file_path)
                    elif file_path.suffix.lower() == '.txt':
                        docs = self._load_text(file_path)
                    else:
                        continue

                    documents.extend(docs)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")

        return documents

    def _load_markdown(self, file_path: Path) -> List[Document]:
        """Load and chunk a markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract document ID and metadata from markdown
        doc_id = self._extract_doc_id(content)

        # Convert markdown to plain text but preserve structure
        html = markdown.markdown(content)
        text = self._html_to_text(html)

        # Clean and normalize text
        text = self._clean_text(text)

        # Chunk by headings first, then by size if needed
        chunks = self._chunk_by_headings(content, file_path, doc_id)

        return chunks

    def _load_pdf(self, file_path: Path) -> List[Document]:
        """Load and chunk a PDF file."""
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n\n"

        text = self._clean_text(text)
        doc_id = self._extract_doc_id_from_filename(file_path)

        return self._chunk_text(text, file_path, doc_id)

    def _load_html(self, file_path: Path) -> List[Document]:
        """Load and chunk an HTML file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()

        text = self._html_to_text(html)
        text = self._clean_text(text)
        doc_id = self._extract_doc_id_from_filename(file_path)

        return self._chunk_text(text, file_path, doc_id)

    def _load_text(self, file_path: Path) -> List[Document]:
        """Load and chunk a text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        text = self._clean_text(text)
        doc_id = self._extract_doc_id_from_filename(file_path)

        return self._chunk_text(text, file_path, doc_id)

    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text."""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)

        # Replace multiple newlines with double newline
        text = re.sub(r'\n\n+', '\n\n', text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text

    def _extract_doc_id(self, content: str) -> str:
        """Extract document ID from markdown content."""
        # Look for pattern like "Document ID: POL-001"
        match = re.search(r'\*\*Document ID\*\*:\s*([A-Z]+-\d+)', content)
        if match:
            return match.group(1)
        return "UNKNOWN"

    def _extract_doc_id_from_filename(self, file_path: Path) -> str:
        """Generate document ID from filename."""
        return file_path.stem.upper()

    def _chunk_by_headings(self, content: str, file_path: Path, doc_id: str) -> List[Document]:
        """
        Chunk markdown content by headings.

        This preserves document structure by keeping sections together.
        """
        chunks = []

        # Split by h1 and h2 headings
        sections = re.split(r'\n(#{1,2}\s+.+)\n', content)

        current_chunk = ""
        current_heading = ""

        for i, section in enumerate(sections):
            if re.match(r'#{1,2}\s+', section):
                # This is a heading
                if current_chunk and len(current_chunk) > 100:
                    # Save previous chunk
                    chunks.append(Document(
                        content=current_chunk.strip(),
                        metadata={
                            "source": str(file_path.name),
                            "doc_id": doc_id,
                            "heading": current_heading,
                            "file_path": str(file_path)
                        }
                    ))
                    current_chunk = ""

                current_heading = section.strip('# ').strip()
                current_chunk = section + "\n"
            else:
                # This is content
                current_chunk += section

                # If chunk is getting too large, split it
                if len(current_chunk) > self.chunk_size * 1.5:
                    sub_chunks = self._chunk_text_simple(current_chunk, file_path, doc_id, current_heading)
                    chunks.extend(sub_chunks)
                    current_chunk = ""

        # Add final chunk
        if current_chunk and len(current_chunk) > 100:
            chunks.append(Document(
                content=current_chunk.strip(),
                metadata={
                    "source": str(file_path.name),
                    "doc_id": doc_id,
                    "heading": current_heading,
                    "file_path": str(file_path)
                }
            ))

        return chunks

    def _chunk_text(self, text: str, file_path: Path, doc_id: str, heading: str = "") -> List[Document]:
        """Chunk text by size with overlap."""
        return self._chunk_text_simple(text, file_path, doc_id, heading)

    def _chunk_text_simple(self, text: str, file_path: Path, doc_id: str, heading: str = "") -> List[Document]:
        """Simple text chunking with overlap."""
        chunks = []

        # Split by paragraphs first
        paragraphs = text.split('\n\n')

        current_chunk = ""

        for para in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(para) > self.chunk_size:
                if current_chunk:
                    chunks.append(Document(
                        content=current_chunk.strip(),
                        metadata={
                            "source": str(file_path.name),
                            "doc_id": doc_id,
                            "heading": heading,
                            "file_path": str(file_path)
                        }
                    ))

                    # Start new chunk with overlap from previous chunk
                    words = current_chunk.split()
                    overlap_words = words[-int(len(words) * (self.chunk_overlap / self.chunk_size)):]
                    current_chunk = ' '.join(overlap_words) + '\n\n' + para
                else:
                    current_chunk = para
            else:
                current_chunk += '\n\n' + para if current_chunk else para

        # Add final chunk
        if current_chunk:
            chunks.append(Document(
                content=current_chunk.strip(),
                metadata={
                    "source": str(file_path.name),
                    "doc_id": doc_id,
                    "heading": heading,
                    "file_path": str(file_path)
                }
            ))

        return chunks


if __name__ == "__main__":
    # Test document processing
    processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
    docs = processor.load_documents("data/policies")

    print(f"Loaded {len(docs)} document chunks")

    # Show sample chunks
    for i, doc in enumerate(docs[:3]):
        print(f"\n--- Chunk {i+1} ---")
        print(f"Source: {doc.metadata['source']}")
        print(f"Doc ID: {doc.metadata['doc_id']}")
        print(f"Heading: {doc.metadata.get('heading', 'N/A')}")
        print(f"Content length: {len(doc.content)} chars")
        print(f"Content preview: {doc.content[:200]}...")
