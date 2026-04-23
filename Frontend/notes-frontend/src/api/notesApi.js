import api from "./axios";

export const getNotes = () => api.get("/notes/user_notes");
export const createNote = (data) => api.post("/notes", data);
export const deleteNote = (id) => api.delete(`/notes/delete_notes/${id}`);