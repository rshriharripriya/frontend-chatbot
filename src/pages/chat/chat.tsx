import { useState } from 'react';

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
        // Attempt to pull FastAPI error detail from response JSON
        let errorMsg = `Error: ${res.status}`;
        try {
          const errorData = await res.json();
          errorMsg += errorData.detail
            ? ` - ${JSON.stringify(errorData.detail)}`
            : ` - ${JSON.stringify(errorData)}`;
        } catch {
          // Could not parse error details
        }
        throw new Error(errorMsg);
      }

      const data = await res.json();
      setResponse(data.output);
    } catch (error) {
      setResponse(error.message);
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
          <div className="message bot-message">
            {response}
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
