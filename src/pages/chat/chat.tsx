import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const formatMarkdown = (text: string): string => {
  // Fix: Remove line breaks between ** and numbered lists
  text = text.replace(/\*\*\n\s*(\d+\.)/g, '** $1');

  // Fix: Remove line breaks in bold text that got split
  text = text.replace(/\*\*\n\s+([^*]+)\*\*/g, '** $1 **');

  // Fix headers followed by content (### Header: * item)
  text = text.replace(/(\*{1,3}[^*]+\*{1,3}:)\s+(\*)/g, '$1\n\n$2');

  // Fix multiple list items on same line (** - text ** - text)
  text = text.replace(/(\*\*[^\n]*?\*\*)\s+(\*\*)/g, '$1\n');

  // Fix numbered lists followed by text (* **Number.**)
  text = text.replace(/(\d+\.\s+\*\*[^*]+\*\*[^*]*?\*\*[^*]+\*\*)\s+(\d+\.)/g, '$1\n$2');

  // Ensure headers have blank lines before them
  text = text.replace(/([^\n])\n(#{1,6}\s+)/g, '$1\n\n$2');

  // Ensure list items have newlines (but not in bold text)
  text = text.replace(/(\*\s+[^\n*]+)\s+(\*\s+)/g, '$1\n$2');

  // Fix bold text followed by dash or bullet without line break
  text = text.replace(/(\*\*[^*]+\*\*:)\s+([*-])/g, '$1\n$2');

  // Add line breaks before numbered lists if missing
  text = text.replace(/([^\n])\n(\d+\.)/g, '$1\n\n$2');

  // Add line breaks before unordered lists if missing (not in bold)
  text = text.replace(/([^:\n*])\s+(\*\s+[^*])/g, '$1\n$2');

  // Ensure paragraphs are separated
  text = text.replace(/([.!?])\s+([A-Z])/g, '$1\n\n$2');

  return text;
};


export default function ChatInterface() {
  const [userInput, setUserInput] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [showSkeleton, setShowSkeleton] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    setLoading(true);
    setResponse('');
    setShowSkeleton(true);

    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: userInput })
      });

      if (!res.ok) {
        let errorMsg = `Error: ${res.status}`;
        try {
          const errorData = await res.json();
          errorMsg += errorData.detail ? ` - ${errorData.detail}` : '';
        } catch {}
        setResponse(errorMsg);
        setLoading(false);
        setShowSkeleton(false);
        return;
      }

      const data = await res.json();
      const formattedOutput = formatMarkdown(data.output);

      setShowSkeleton(false);
      setResponse(formattedOutput);
      setLoading(false);
    } catch (error) {
      setResponse(`Error: ${error.message}`);
      setLoading(false);
      setShowSkeleton(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-window">
        {userInput && (
          <div className="message user-message">
            {userInput}
          </div>
        )}

        {showSkeleton && (
          <div className="message bot-message">
            <div className="skeleton-paragraph">
              <div className="skeleton-line long"></div>
              <div className="skeleton-line medium"></div>
              <div className="skeleton-line long"></div>
              <div className="skeleton-line short"></div>
            </div>
          </div>
        )}

        {!showSkeleton && response && (
          <div className="message bot-message markdown-response">
            <ReactMarkdown
              components={{
                h1: ({ children }) => <h1>{children}</h1>,
                h2: ({ children }) => <h2>{children}</h2>,
                h3: ({ children }) => <h3>{children}</h3>,
                h4: ({ children }) => <h4>{children}</h4>,
                h5: ({ children }) => <h5>{children}</h5>,
                h6: ({ children }) => <h6>{children}</h6>,
                p: ({ children }) => <p>{children}</p>,
                ul: ({ children }) => <ul>{children}</ul>,
                ol: ({ children }) => <ol>{children}</ol>,
                li: ({ children }) => <li>{children}</li>,
                code: ({ children }) => <code>{children}</code>,
                pre: ({ children }) => <pre>{children}</pre>,
                blockquote: ({ children }) => <blockquote>{children}</blockquote>,
                hr: () => <hr />,
              }}
            >
              {response}
            </ReactMarkdown>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Ask me something..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
    </div>
  );
}
