package algorithms;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Kiểm thử thuật toán Mergesort")
public class MergesortTest {

    @Test
    @DisplayName("Mergesort thuần (baseline)")
    public void testPureMergesort() {
        Integer[] a = {9, 4, 7, 2, 8, 1, 5, 3, 6};
        Mergesort.sort(a);
        assertArrayEquals(new Integer[]{1, 2, 3, 4, 5, 6, 7, 8, 9}, a);
    }

    @ParameterizedTest(name = "Mergesort với CUTOFF = {0}")
    @ValueSource(ints = {1, 2, 5, 7, 10, 15, 20})
    public void testMergesortWithCutoff(int cutoff) {
        Integer[] a = {15, 3, 2, 56, 42, 11, 89, 7, 0, 99, 1};
        Mergesort.sort(a, cutoff);
        for (int i = 0; i < a.length - 1; i++) {
            assertTrue(a[i] <= a[i + 1], "Mảng chưa được sắp xếp đúng tại vị trí " + i);
        }
    }

    @Test
    @DisplayName("Mảng nhiều phần tử trùng lặp")
    public void testManyDuplicates() {
        Integer[] a = {3, 1, 2, 1, 3, 2, 1, 2, 3};
        Mergesort.sort(a, 10);
        assertArrayEquals(new Integer[]{1, 1, 1, 2, 2, 2, 3, 3, 3}, a);
    }
}
