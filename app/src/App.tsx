import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Brass Editorial</h1>
      <p>Foundation scaffold — offline single-file build.</p>
      <button
        type="button"
        onClick={() => setCount((count) => count + 1)}
        style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
      >
        Count is {count}
      </button>
    </div>
  )
}

export default App
