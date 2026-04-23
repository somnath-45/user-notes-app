import { useState } from "react";

export default function NoteForm({ onSubmit, userId }) {
  const [form, setForm] = useState({
    topic: "",
    text: ""
  });

  const handleSubmit = () => {
    onSubmit({ ...form, user_id: userId });
  };

  return (
    <div>
      <input
        placeholder="topic"
        onChange={(e) => setForm({ ...form, topic: e.target.value })}
      />

      <textarea
        placeholder="text"
        onChange={(e) => setForm({ ...form, text: e.target.value })}
      />

      <button onClick={handleSubmit}>Add Note</button>
    </div>
  );
}