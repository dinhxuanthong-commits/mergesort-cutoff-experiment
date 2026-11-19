package algorithms;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Kiểm thử thuật toán Insertionsort")
public class InsertionsortTest {

    @Test
    @DisplayName("Sắp xếp mảng ngẫu nhiên")
    public void testSortRandom() {
        Integer[] a = {5, 2, 8, 1, 9, 3, 7, 4, 6};
        Insertionsort.sort(a);
        assertArrayEquals(new Integer[]{1, 2, 3, 4, 5, 6, 7, 8, 9}, a);
    }

    @Test
    @DisplayName("Sắp xếp đoạn con [lo..hi]")
    public void testSortSubarray() {
        Integer[] a = {999, 5, 3, 1, 4, 888};
        Insertionsort.sort(a, 1, 4);
        assertEquals(999, a[0]);
        assertEquals(888, a[5]);
        assertArrayEquals(new Integer[]{1, 3, 4, 5}, new Integer[]{a[1], a[2], a[3], a[4]});
    }

    @Test
    @DisplayName("Mảng 1 phần tử")
    public void testSingleElement() {
        Integer[] a = {42};
        Insertionsort.sort(a);
        assertArrayEquals(new Integer[]{42}, a);
    }

    @Test
    @DisplayName("Mảng đã có thứ tự")
    public void testAlreadySorted() {
        Integer[] a = {1, 2, 3, 4, 5};
        Insertionsort.sort(a);
        assertArrayEquals(new Integer[]{1, 2, 3, 4, 5}, a);
    }

    @Test
    @DisplayName("Mảng giảm dần")
    public void testReversed() {
        Integer[] a = {5, 4, 3, 2, 1};
        Insertionsort.sort(a);
        assertArrayEquals(new Integer[]{1, 2, 3, 4, 5}, a);
    }
}
