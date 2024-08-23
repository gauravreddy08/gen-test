
import java.util.ArrayList;
import java.util.List;

public class Library {
    private final BookManager bookManager;
    private final UserManager userManager;
    private final List<BorrowRecord> borrowRecords;

    public Library() {
        this.bookManager = new BookManager();
        this.userManager = new UserManager();
        this.borrowRecords = new ArrayList<>();
    }

    public void addBook(Book book) {
        bookManager.add(book);
    }

    public void removeBook(Book book) {
        bookManager.remove(book);
    }

    public Book searchBookByTitle(String title) {
        return bookManager.search(title);
    }

    public void addUser(User user) {
        userManager.add(user);
    }

    public void removeUser(User user) {
        userManager.remove(user);
    }

    public User searchUserById(String id) {
        return userManager.search(id);
    }

    public void borrowBook(User user, Book book) {
        if (!book.isBorrowed()) {
            BorrowRecord record = new BorrowRecord(book);
            book.setBorrowed(true);
            user.addBorrowRecord(record);
            borrowRecords.add(record);
            System.out.println("Book borrowed successfully.");
        } else {
            System.out.println("Book is already borrowed.");
        }
    }

    public void returnBook(User user, Book book) {
        for (BorrowRecord record : user.getBorrowRecords()) {
            if (record.getBook().equals(book) && record.getReturnDate() == null) {
                record.setReturnDate(java.time.LocalDate.now());
                book.setBorrowed(false);
                System.out.println("Book returned successfully.");
                return;
            }
        }
        System.out.println("Book was not borrowed by the user.");
    }

    public String generateReport(ReportGenerator reportGenerator) {
        return reportGenerator.generateReport();
    }

    public static void main(String[] args) {
        Library library = new Library();
        Book book1 = new Book("Effective Java", "Joshua Bloch", "1234567890");
        User user1 = new User("John Doe", "1");

        library.addBook(book1);
        library.addUser(user1);

        library.borrowBook(user1, book1);
        System.out.println(library.generateReport(new AvailableBooksReport(library.bookManager)));
    }
}
