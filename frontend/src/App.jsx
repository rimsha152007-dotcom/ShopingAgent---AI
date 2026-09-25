import { useEffect, useState } from 'react'

function App() {
  const [status, setStatus] = useState('Loading...')
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetch(`${apiUrl}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus('Error connecting to backend'))
  }, [apiUrl])

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white p-6 rounded-lg shadow-md text-center max-w-md w-full">
        <h1 className="text-2xl font-bold mb-4 text-gray-800">ShopAgent AI Frontend</h1>
        <p className="text-gray-600 mb-2">Backend Status:</p>
        <div className="inline-block px-4 py-2 bg-blue-100 text-blue-800 font-semibold rounded-full">
          {status}
        </div>
      </div>
    </div>
  )
}

export default App
