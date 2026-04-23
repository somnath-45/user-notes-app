import { useEffect, useState } from "react";
import { getNotes, createNote, deleteNote } from "../api/notesApi";

export default function Notes() {
  const [notes, setNotes] = useState([]);
  const [form, setForm] = useState({ topic: "", text: "" });

  const fetchNotes = async () => {
    const res = await getNotes();
    setNotes(res.data);
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const addNote = async () => {
    await createNote(form);
    setForm({ topic: "", text: "" });
    fetchNotes();
  };

  const removeNote = async (id) => {
    await deleteNote(id);
    fetchNotes();
  };

  const logout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div className="notes-container">
      <h2>My Notes</h2>
      <button onClick={logout}>Logout</button>

      <div className="note-form">
        <input
          placeholder="Topic"
          value={form.topic}
          onChange={(e) =>
            setForm({ ...form, topic: e.target.value })
          }
        />

        <input
          placeholder="Text"
          value={form.text}
          onChange={(e) =>
            setForm({ ...form, text: e.target.value })
          }
        />

        <button onClick={addNote}>Add Note</button>
      </div>

      <div className="notes-list">
        {notes.map((n) => (
          <div key={n.id} className="note-card">
            <h4>{n.topic}</h4>
            <p>{n.text}</p>
            <button onClick={() => removeNote(n.id)}>
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}