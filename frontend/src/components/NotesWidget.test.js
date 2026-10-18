import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { NotificationProvider } from '../context/NotificationContext';
import NotesWidget from './NotesWidget';

const renderNotesWidget = (props) => render(
    <NotificationProvider>
        <NotesWidget {...props} isEditMode viewOnly={false} />
    </NotificationProvider>
);

describe('NotesWidget', () => {
    beforeEach(() => {
        localStorage.clear();
    });

    it('keeps a newly added note when stale props arrive and deletion is cancelled', async () => {
        const onUpdateNotes = vi.fn();
        const props = { notes: [], onUpdateNotes };
        const { rerender } = renderNotesWidget(props);

        fireEvent.click(screen.getByRole('button', { name: /add note/i }));
        expect(screen.getByDisplayValue('New Note')).toBeInTheDocument();

        rerender(
            <NotificationProvider>
                <NotesWidget notes={[]} onUpdateNotes={onUpdateNotes} isEditMode viewOnly={false} />
            </NotificationProvider>
        );

        expect(screen.getByDisplayValue('New Note')).toBeInTheDocument();
        fireEvent.click(screen.getByTitle('Delete Note'));
        fireEvent.click(screen.getByRole('button', { name: /cancel/i }));

        expect(screen.getByDisplayValue('New Note')).toBeInTheDocument();
        expect(onUpdateNotes).toHaveBeenLastCalledWith(
            expect.arrayContaining([expect.objectContaining({ title: 'New Note' })])
        );
    });

    it('removes a note only after deletion is confirmed', async () => {
        renderNotesWidget({
            notes: [{ id: 1, title: 'Keep or delete?', content: '', height: 150 }],
            onUpdateNotes: vi.fn()
        });

        fireEvent.click(screen.getByTitle('Delete Note'));
        expect(screen.getByDisplayValue('Keep or delete?')).toBeInTheDocument();
        fireEvent.click(screen.getByRole('button', { name: /confirm/i }));

        await waitFor(() => {
            expect(screen.queryByDisplayValue('Keep or delete?')).not.toBeInTheDocument();
        });
    });
});
