# Testing Checklist - Notes App Frontend

Complete this checklist after setting up and running the frontend with a working backend.

## Setup (Prerequisites)

- [ ] Backend API running at `http://localhost:8000/api`
- [ ] Backend database has test data or is empty
- [ ] Frontend installed: `npm install` in `frontend/` directory
- [ ] Frontend running: `npm run dev`
- [ ] Browser open to `http://localhost:5173`

## View and Load Tests

### Initial Load
- [ ] Page loads without errors
- [ ] Header displays "Notes App" title
- [ ] "+ New Note" button is visible
- [ ] Page shows loading spinner briefly
- [ ] If no notes exist, empty state displays
- [ ] If notes exist, they load in grid layout

### Note Display
- [ ] Each note card shows title
- [ ] Content preview shows first 100 characters
- [ ] Long content shows ellipsis (...)
- [ ] Tags display as blue pill badges
- [ ] Updated date appears in small text
- [ ] Edit and Delete buttons present on each card
- [ ] Notes display in responsive grid (1 column mobile, 3 columns desktop)

## Create Note Tests

### Form Opening
- [ ] "+ New Note" button opens modal
- [ ] Modal has close button (×)
- [ ] Modal shows "New Note" heading
- [ ] Form fields are empty

### Form Fields
- [ ] Title field accepts text
- [ ] Content textarea accepts multi-line text
- [ ] Tags field accepts comma-separated values
- [ ] Tab navigation works between fields
- [ ] All fields accept Unicode/special characters

### Form Validation
- [ ] Cannot submit with empty title
- [ ] Cannot submit with empty content
- [ ] Error message shows for empty fields
- [ ] Error is red and clear
- [ ] Can add tags (optional)

### Form Submission
- [ ] "Save Note" button is disabled while saving
- [ ] Button shows "Saving..." text while submitting
- [ ] Success: Modal closes automatically
- [ ] New note appears in list
- [ ] List updates immediately (no page refresh needed)
- [ ] Note has correct title and content
- [ ] Tags are parsed correctly from comma-separated input

### Form Error Handling
- [ ] Network error shows appropriate message
- [ ] Error stays visible, form doesn't close
- [ ] Can retry after error
- [ ] Cancel button always works

### Cancel Button
- [ ] Cancel button closes modal without saving
- [ ] Form data is lost (doesn't persist)
- [ ] Modal closes properly

## Edit Note Tests

### Opening Edit Form
- [ ] Edit button on note card opens modal
- [ ] Modal shows "Edit Note" heading
- [ ] Title field prefilled with current title
- [ ] Content field prefilled with current content
- [ ] Tags field shows tags as comma-separated
- [ ] All existing data is correct

### Editing
- [ ] Can change title
- [ ] Can change content
- [ ] Can modify tags
- [ ] Can add new tags
- [ ] Can remove tags (by editing comma-separated list)
- [ ] Validation still works (title and content required)

### Save Changes
- [ ] "Save Note" saves changes
- [ ] Modal closes after save
- [ ] Updated note appears in list
- [ ] Old version is replaced (not duplicated)
- [ ] Tags update correctly
- [ ] Last updated date changes

## Delete Note Tests

### Delete Button
- [ ] Delete button opens confirmation
- [ ] Confirmation asks "Are you sure?"
- [ ] Has Cancel option
- [ ] Has Delete/Confirm option

### Delete Confirmation
- [ ] Cancel button prevents deletion
- [ ] Confirm button deletes note
- [ ] Deleted note disappears from list
- [ ] List updates immediately
- [ ] No modal shown after delete (or closes automatically)
- [ ] Empty state appears if all notes deleted

### Delete Error Handling
- [ ] Network error during delete shows message
- [ ] User can retry delete
- [ ] Note doesn't disappear on error

## Tag Filter Tests

### Tag Filter Display
- [ ] Tag filter section appears when notes have tags
- [ ] "All Notes" button appears first
- [ ] All unique tags from notes appear as buttons
- [ ] Tags are sorted alphabetically
- [ ] No duplicate tags show

### Filter Functionality
- [ ] Clicking tag filters notes to only those with tag
- [ ] Multiple notes with same tag all show
- [ ] Notes without selected tag don't show
- [ ] "All Notes" button clears filter
- [ ] Selected tag button appears highlighted (blue)
- [ ] Non-selected buttons appear gray

### Filter with Empty Results
- [ ] Filter to tag with no matching notes
- [ ] Empty state shows "No notes found"
- [ ] Can click "All Notes" to see notes again

## UI/UX Tests

### Responsiveness
- [ ] Layout works on mobile (375px width)
- [ ] Layout works on tablet (768px width)
- [ ] Layout works on desktop (1200px+ width)
- [ ] Grid changes column count appropriately

### Visual Design
- [ ] Header has gradient blue background
- [ ] Buttons are consistent color (blue for primary)
- [ ] Delete buttons are red
- [ ] Hover effects work on buttons
- [ ] Text is readable on all backgrounds
- [ ] Modal overlay is visible and dark

### Loading States
- [ ] Loading spinner shows initially
- [ ] Save button disabled while loading
- [ ] Loading text appears while fetching

### Error States
- [ ] Error messages are clear and red
- [ ] Error messages suggest action (e.g., "Try again")
- [ ] Errors don't block entire page

## Edge Cases

### Empty/Whitespace
- [ ] Can create note with title only (content still required)
- [ ] Whitespace-only content fails validation
- [ ] Tags with only commas and spaces work correctly
- [ ] Tags strip leading/trailing whitespace

### Long Content
- [ ] Very long title truncates on card (line-clamp-2)
- [ ] Long content preview truncates (100 chars)
- [ ] Very long note content saves correctly
- [ ] Edit preserves all content

### Special Characters
- [ ] Emoji in titles work
- [ ] Emoji in content works
- [ ] HTML in content (if rendered) is escaped
- [ ] URLs in content display as text

### Tags Edge Cases
- [ ] Single tag works
- [ ] Many tags work (10+)
- [ ] Tag names with spaces work
- [ ] Duplicate tags deduplicate in form
- [ ] Filtering with many tags works smoothly

## Performance Tests

### Initial Load
- [ ] Page loads in under 3 seconds
- [ ] No console errors on load
- [ ] No memory leaks (check DevTools)

### List Performance
- [ ] Large note list (50+) scrolls smoothly
- [ ] Filtering updates instantly
- [ ] No lag when switching tags

### Form Performance
- [ ] Modal opens instantly
- [ ] Form field inputs respond immediately
- [ ] No lag in typing

## Browser Tests

- [ ] Chrome/Edge - all tests pass
- [ ] Firefox - all tests pass
- [ ] Safari - all tests pass (if available)

## Accessibility Tests

- [ ] Keyboard navigation works (Tab/Shift+Tab)
- [ ] Button focus states visible
- [ ] Modal is accessible
- [ ] Form labels exist
- [ ] Color contrast is sufficient
- [ ] Error messages are visible to screen readers

## Summary

Total test scenarios: 80+

After testing:
- [ ] All critical path tests pass (Create, Read, Edit, Delete)
- [ ] All tag filter tests pass
- [ ] No console errors
- [ ] No console warnings about deprecated APIs
- [ ] App is ready for integration testing with backend team
