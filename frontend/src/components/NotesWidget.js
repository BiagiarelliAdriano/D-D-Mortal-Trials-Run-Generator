import React, { useState, useEffect, useRef } from 'react';
import { useNotification } from '../context/NotificationContext';

const NotesWidget = ({ notes, onUpdateNotes, isEditMode, viewOnly }) => {
    const [localNotes, setLocalNotes] = useState(notes || []);
    const { confirm } = useNotification();

    useEffect(() => {
        let hasUnsaved = false;
        const initialNotes = (notes || []).map(n => {
            const unsavedContent = localStorage.getItem(`unsaved_note_content_${n.id}`);
            const unsavedTitle = localStorage.getItem(`unsaved_note_title_${n.id}`);
            
            let updated = { ...n };

            // If the database already matches our local backup, it means the save succeeded! We can safely delete the backup.
            if (unsavedContent === n.content) {
                localStorage.removeItem(`unsaved_note_content_${n.id}`);
            } else if (unsavedContent !== null) {
                hasUnsaved = true;
                updated.content = unsavedContent;
            }
            
            if (unsavedTitle === n.title) {
                localStorage.removeItem(`unsaved_note_title_${n.id}`);
            } else if (unsavedTitle !== null) {
                hasUnsaved = true;
                updated.title = unsavedTitle;
            }

            return updated;
        });

        setLocalNotes(initialNotes);

        // If we recovered data that the database doesn't have yet, sync it back.
        // We DO NOT delete the backup here. We keep it until the next load where it matches the database.
        if (hasUnsaved) {
            onUpdateNotes(initialNotes);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [notes]);
    const handleAddNote = () => {
        if (localNotes.length >= 100) return;
        const newNote = {
            id: Date.now(),
            title: "New Note",
            content: "",
            height: 150
        };
        const updated = [...localNotes, newNote];
        setLocalNotes(updated);
        onUpdateNotes(updated);
    };

    const handleUpdateNote = (id, field, value) => {
        let finalValue = value;
        if (field === 'title' && value && value.length > 45) {
            finalValue = value.substring(0, 45);
        }

        setLocalNotes(prev => {
            const updated = prev.map(n => n.id === id ? { ...n, [field]: finalValue } : n);
            // We call onUpdateNotes with the NEWly calculated updated array
            onUpdateNotes(updated);
            return updated;
        });
    };

    const handleDeleteNote = async (id) => {
        const isConfirmed = await confirm("Delete this note?");
        if (isConfirmed) {
            const updated = localNotes.filter(n => n.id !== id);
            setLocalNotes(updated);
            onUpdateNotes(updated);
        }
    };

    const execCommand = (command, value = null) => {
        document.execCommand(command, false, value);
    };

    return (
        <div className="notes-widget-container">
            <div className="notes-header">
                <h3>Notes ({localNotes.length}/100)</h3>
                {!viewOnly && (
                    <button className="add-note-btn" onClick={handleAddNote} disabled={localNotes.length >= 100}>
                        <i className="fa-solid fa-plus"></i> Add Note
                    </button>
                )}
            </div>
            <div className="notes-list scrollable">
                {localNotes.length === 0 ? (
                    <p className="no-notes-hint">No notes yet. Click "Add Note" to start writing.</p>
                ) : (
                    localNotes.map(note => (
                        <NoteCard
                            key={note.id}
                            note={note}
                            isEditMode={isEditMode}
                            viewOnly={viewOnly}
                            onUpdate={handleUpdateNote}
                            onDelete={() => handleDeleteNote(note.id)}
                            execCommand={execCommand}
                        />
                    ))
                )}
            </div>
        </div>
    );
};

const NoteCard = ({ note, isEditMode, viewOnly, onUpdate, onDelete, execCommand }) => {
    const cardRef = useRef(null);
    const contentRef = useRef(null);
    const [isResizing, setIsResizing] = useState(false);
    const [localTitle, setLocalTitle] = useState(note.title);
    const saveTimeout = useRef(null);
    const titleTimeout = useRef(null);

    // Sync contenteditable with note.content
    useEffect(() => {
        if (contentRef.current && contentRef.current.innerHTML !== note.content) {
            contentRef.current.innerHTML = note.content;
        }
    }, [note.content]);

    // Sync local title if parent changes
    useEffect(() => {
        setLocalTitle(note.title);
    }, [note.title]);

    const handleContentChange = () => {
        if (saveTimeout.current) {
            clearTimeout(saveTimeout.current);
            saveTimeout.current = null;
        }
        if (contentRef.current && contentRef.current.innerHTML !== note.content) {
            onUpdate(note.id, 'content', contentRef.current.innerHTML);
        }
    };

    const handleInput = () => {
        if (saveTimeout.current) clearTimeout(saveTimeout.current);
        
        if (contentRef.current) {
            localStorage.setItem(`unsaved_note_content_${note.id}`, contentRef.current.innerHTML);
        }

        saveTimeout.current = setTimeout(() => {
            if (contentRef.current && contentRef.current.innerHTML !== note.content) {
                onUpdate(note.id, 'content', contentRef.current.innerHTML);
            }
            saveTimeout.current = null;
        }, 1000);
    };

    const startResize = (e) => {
        if (!isEditMode) return;
        e.preventDefault();

        const initialY = e.pageY;
        const initialHeight = cardRef.current ? cardRef.current.offsetHeight : (note.height || 150);
        setIsResizing(true);

        const handleMouseMove = (moveEvent) => {
            const delta = moveEvent.pageY - initialY;
            const newHeight = Math.max(150, initialHeight + delta);
            onUpdate(note.id, 'height', newHeight);
        };

        const handleMouseUp = () => {
            setIsResizing(false);
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };

        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
    };

    return (
        <div 
            ref={cardRef}
            className={`note-card premium-card ${isEditMode ? 'is-editing' : ''} ${isResizing ? 'resizing' : ''}`} 
            style={{ minHeight: (note.height || 150) + 'px', height: 'auto' }}
        >
            <div className="note-card-header">
                {viewOnly ? (
                    <h4 className="note-title-view">{note.title}</h4>
                ) : (
                    <input
                        type="text"
                        className="note-title-input"
                        value={localTitle}
                        maxLength={45}
                        onChange={(e) => {
                            let val = e.target.value;
                            if (val.length > 45) {
                                val = val.substring(0, 45);
                                e.target.value = val; // The absolute only way to fix React controlled input bailout
                            }
                            setLocalTitle(val);
                            localStorage.setItem(`unsaved_note_title_${note.id}`, val);
                            
                            if (titleTimeout.current) clearTimeout(titleTimeout.current);
                            titleTimeout.current = setTimeout(() => {
                                onUpdate(note.id, 'title', val);
                                titleTimeout.current = null;
                            }, 500);
                        }}
                        onBlur={() => {
                            if (titleTimeout.current) {
                                clearTimeout(titleTimeout.current);
                                titleTimeout.current = null;
                            }
                            onUpdate(note.id, 'title', localTitle);
                        }}
                        placeholder="Note Title..."
                    />
                )}
                {!viewOnly && (
                    <span className="note-title-counter" style={{ fontSize: '0.75rem', color: '#888', marginLeft: '10px' }}>
                        {localTitle.length}/45
                    </span>
                )}
                {!viewOnly && (
                    <button 
                        type="button" 
                        className="note-delete-btn" 
                        onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            onDelete();
                        }} 
                        title="Delete Note"
                    >
                        <i className="fa-solid fa-trash-can"></i>
                    </button>
                )}
            </div>

            {!viewOnly && (
                <div className="note-toolbar">
                    <button onMouseDown={(e) => { e.preventDefault(); execCommand('bold'); }} title="Bold"><i className="fa-solid fa-bold"></i></button>
                    <button onMouseDown={(e) => { e.preventDefault(); execCommand('italic'); }} title="Italic"><i className="fa-solid fa-italic"></i></button>
                    <button onMouseDown={(e) => { e.preventDefault(); execCommand('underline'); }} title="Underline"><i className="fa-solid fa-underline"></i></button>
                    <button onMouseDown={(e) => { e.preventDefault(); execCommand('strikethrough'); }} title="Strikethrough"><i className="fa-solid fa-strikethrough"></i></button>
                    <div className="toolbar-sep"></div>
                    <button onMouseDown={(e) => { e.preventDefault(); execCommand('insertUnorderedList'); }} title="Bullet List"><i className="fa-solid fa-list-ul"></i></button>
                    <button onMouseDown={(e) => { e.preventDefault(); execCommand('insertOrderedList'); }} title="Numbered List"><i className="fa-solid fa-list-ol"></i></button>
                    <div className="toolbar-sep"></div>
                    <button onMouseDown={(e) => { e.preventDefault(); execCommand('removeFormat'); }} title="Clear Formatting"><i className="fa-solid fa-eraser"></i></button>
                </div>
            )}

            <div
                ref={contentRef}
                className="note-content-editor"
                contentEditable={!viewOnly}
                onBlur={handleContentChange}
                onInput={handleInput}
                placeholder="Write your note here..."
                style={{
                    minHeight: (note.height ? note.height - 80 : 100) + 'px',
                    pointerEvents: viewOnly ? 'none' : 'auto',
                    height: 'auto',
                    overflow: 'hidden', // Prevent 'falling through' the card background
                    wordBreak: 'break-word',
                    overflowWrap: 'break-word'
                }}
            />

            {isEditMode && (
                <div className="note-resize-handle" onMouseDown={startResize}>
                    <i className="fa-solid fa-grip-lines"></i>
                </div>
            )}
        </div>
    );
};

export default NotesWidget;
