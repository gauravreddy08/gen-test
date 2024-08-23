
import java.time.LocalDate;

public class BorrowRecord {
    private Book book;
    private LocalDate borrowDate;
    private LocalDate returnDate;

    public BorrowRecord(Book book) {
        this.book = book;
        this.borrowDate = LocalDate.now();
    }

    public Book getBook() {
        return book;
    }

    public LocalDate getBorrowDate() {
        return borrowDate;
    }

    public LocalDate getReturnDate() {
        return returnDate;
    }

    public void setReturnDate(LocalDate returnDate) {
        this.returnDate = returnDate;
    }

    public double calculateFine() {
        if (returnDate == null) {
            return 0.0;
        }
        long daysLate = java.time.temporal.ChronoUnit.DAYS.between(borrowDate, returnDate) - 14;
        return daysLate > 0 ? daysLate * 0.5 : 0.0;
    }
}
