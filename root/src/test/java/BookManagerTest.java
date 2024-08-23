import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.Map;
import java.util.HashMap;

class BookManagerTest {
    private BookManager bookManager;
    private Book book1;
    private Book book2;

    @BeforeEach
    void setUp() {
        bookManager = new BookManager();
        book1 = new Book("Title1", "Author1", "ISBN1");
        book2 = new Book("Title2", "Author2", "ISBN2");
    }

    @Test
    void testAdd() {
        bookManager.add(book1);
        assertEquals(book1, bookManager.books.get("ISBN1"));
    }

    @Test
    void testRemove() {
        bookManager.add(book1);
        bookManager.remove(book1);
        assertNull(bookManager.books.get("ISBN1"));
    }

    @Test
    void testSearch() {
        bookManager.add(book1);
        assertEquals(book1, bookManager.search("Title1"));
    }

    @Test
    void testSearchNonExistingBook() {
        assertNull(bookManager.search("NonExistingTitle"));
    }

    @Test
    void testAddDuplicateIsbn() {
        Book duplicateBook = new Book("DuplicateTitle", "Author1", "ISBN1");
        bookManager.add(book1);
        bookManager.add(duplicateBook);
        assertEquals(duplicateBook, bookManager.books.get("ISBN1"));
        // Ensure the map contains only one book with ISBN1 and it is the last one added
        assertEquals(1, bookManager.books.size());
    }

    @Test
    void testRemoveNonExistentBook() {
        bookManager.add(book1);
        bookManager.remove(book2);
        assertEquals(1, bookManager.books.size());
        assertEquals(book1, bookManager.books.get("ISBN1"));
    }

    @Test
    void testSearchCaseInsensitive() {
        bookManager.add(book1);
        assertEquals(book1, bookManager.search("tItLe1"));
    }

    @Test
    void testSearchMultipleBooksSameTitle() {
        Book duplicateTitleBook = new Book("Title1", "DifferentAuthor", "DifferentISBN");
        bookManager.add(book1);
        bookManager.add(duplicateTitleBook);
        assertEquals(book1, bookManager.search("Title1"));
        // Ensure it returns the first book that matches the title
    }

    @Test
    void testAddNullBook() {
        assertThrows(NullPointerException.class, () -> {
            bookManager.add(null);
        });
    }
}