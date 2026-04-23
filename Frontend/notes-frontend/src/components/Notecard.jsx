export default function NoteCard({ note }) {
  return (
    <div style={{ border: "1px solid gray", margin: 10 }}>
      <h3>{note.topic}</h3>
      <p>{note.text}</p>
    </div>
  );
}