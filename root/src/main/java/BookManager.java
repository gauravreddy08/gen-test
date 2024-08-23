
import java.util.HashMap;
import java.util.Map;

public class BookManager implements LibraryOperations<Book> {
    public final Map<String, Book> books = new HashMap<>();

    @Override
    public void add(Book book) {
        books.put(book.getIsbn(), book);
    }

    @Override
    public void remove(Book book) {
        books.remove(book.getIsbn());
    }

    @Override
    public Book search(String title) {
        return books.values().stream()
                .filter(book -> book.getTitle().equalsIgnoreCase(title))
                .findFirst()
                .orElse(null);
    }
}
