import { useEffect, useState } from 'react'
import OBR from '@owlbear-rodeo/sdk'
import './App.css'

function App() {
  const [owlbearStatus, setOwlbearStatus] = useState(
    'Checking Owlbear connection...'
  )
  const [roomId, setRoomId] = useState('')
  const [copyStatus, setCopyStatus] = useState('')

  useEffect(() => {
    if (!OBR.isAvailable) {
      setOwlbearStatus('Not running inside Owlbear Rodeo')
      return
    }

    return OBR.onReady(async () => {
      setOwlbearStatus('Connected to Owlbear Rodeo')

      try {
        const id = OBR.room.id
        setRoomId(id)
      } catch (error) {
        console.error('Could not retrieve the room ID:', error)
        setRoomId('Unable to retrieve room ID')
      }
    })
  }, [])

  async function copyRoomId() {
    try {
      await navigator.clipboard.writeText(roomId)
      setCopyStatus('Copied!')
    } catch (error) {
      console.error('Could not copy room ID:', error)
      setCopyStatus('Copy failed')
    }
  }

  return (
    <main className="app">
      <header className="app-header">
        <img
          src="/icon.svg"
          alt="The Mortal Trials logo"
          className="app-logo"
        />

        <div>
          <h1>The Mortal Trials</h1>
          <p>YOUR ADVENTURE STARTS HERE</p>
        </div>
      </header>

      <section className="welcome">
        <h2>Welcome, Trialseeker.</h2>
        <p>
          Prepare your character, join your party, and enter the Tower
          of the Gods.
        </p>
      </section>

      <section className="menu">
        <button className="menu-button" type="button">
          <span className="menu-icon">⚔</span>
          <span className="menu-text">
            <strong>Characters</strong>
            <small>Access your adventurers</small>
          </span>
          <span className="menu-arrow">›</span>
        </button>

        <button className="menu-button" type="button">
          <span className="menu-icon">◈</span>
          <span className="menu-text">
            <strong>My Runs</strong>
            <small>Join or manage your Runs</small>
          </span>
          <span className="menu-arrow">›</span>
        </button>

        <button className="menu-button" type="button">
          <span className="menu-icon">🎲</span>
          <span className="menu-text">
            <strong>Dice Roller</strong>
            <small>Roll for your next trial</small>
          </span>
          <span className="menu-arrow">›</span>
        </button>
      </section>

      <footer className="app-footer">
        <p>{owlbearStatus}</p>

        {roomId && (
          <div className="room-info">
            <label htmlFor="room-id">Room ID</label>
            <input
              id="room-id"
              className="room-id-input"
              type="text"
              value={roomId}
              readOnly
              onFocus={(event) => event.target.select()}
            />
            <p>Select the ID above and press Ctrl+C to copy it.</p>
          </div>
        )}

        <span>THE TOWER AWAITS</span>
      </footer>
    </main>
  )
}

export default App