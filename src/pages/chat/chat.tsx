import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

// Formatter to fix markdown without line breaks
const formatMarkdown = (text: string): string => {
  // Replace common markdown patterns that are missing line breaks

  // Fix headers followed by content (### Header: * item)
  text = text.replace(/(\*{1,3}[^*]+\*{1,3}:)\s+(\*)/g, '$1\n\n$2');

  // Fix multiple list items on same line (** - text ** - text)
  text = text.replace(/(\*\*[^\n]*?\*\*)\s+(\*\*)/g, '$1\n');

  // Fix numbered lists followed by text (* **Number.**)
  text = text.replace(/(\d+\.\s+\*\*[^*]+\*\*[^*]*?\*\*[^*]+\*\*)\s+(\d+\.)/g, '$1\n$2');

  // Ensure headers have blank lines before them
  text = text.replace(/([^\n])\n(#{1,6}\s+)/g, '$1\n\n$2');

  // Ensure list items have newlines
  text = text.replace(/(\*\s+[^\n]*?[^\n\*])\s+(\*\s+)/g, '$1\n$2');

  // Fix bold text followed by dash or bullet without line break
  text = text.replace(/(\*\*[^*]+\*\*:)\s+([*-])/g, '$1\n$2');

  // Add line breaks before numbered lists if missing
  text = text.replace(/([^\n])\n(\d+\.)/g, '$1\n\n$2');

  // Add line breaks before unordered lists if missing
  text = text.replace(/([^:\n])\s+(\*\s+)/g, '$1\n$2');

  // Fix dashes followed by text on same line
  text = text.replace(/(-\s+\*\*[^*]+\*\*[^\n]*?)\s+(-\s+)/g, '$1\n$2');

  // Ensure paragraphs are separated
  text = text.replace(/([.!?])\s+([A-Z])/g, '$1\n\n$2');

  return text;
};

export default function ChatInterface() {
  const [userInput, setUserInput] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    setLoading(true);
    setResponse('');

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
        return;
      }

      const data = await res.json();

      // Format the markdown to fix missing line breaks
      const formattedOutput = formatMarkdown(data.output);

      setResponse(formattedOutput);
    } catch (error) {
      setResponse(`Error: ${error.message}`);
    } finally {
      setLoading(false);
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

        {loading && (
          <div className="message bot-message">
            <div className="skeleton-paragraph">
              <div className="skeleton-line long"></div>
              <div className="skeleton-line medium"></div>
              <div className="skeleton-line long"></div>
              <div className="skeleton-line short"></div>
            </div>
          </div>
        )}

        {response && !loading && (
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
