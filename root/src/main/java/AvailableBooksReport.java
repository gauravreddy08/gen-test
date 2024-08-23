
public class AvailableBooksReport implements ReportGenerator {
    private final BookManager bookManager;

    public AvailableBooksReport(BookManager bookManager) {
        this.bookManager = bookManager;
    }

    @Override
    public String generateReport() {
        StringBuilder report = new StringBuilder();
        report.append("Available Books:\n");
        bookManager.books.values().stream()
                .filter(book -> !book.isBorrowed())
                .forEach(book -> report.append(book.getTitle()).append(" by ").append(book.getAuthor()).append("\n"));
        return report.toString();
    }
}
