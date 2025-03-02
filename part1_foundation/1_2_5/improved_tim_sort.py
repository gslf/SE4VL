def calc_min_run(n):
    """
    Calculate the minimum run size for Timsort.
    The idea is to choose a min_run such that the array can be divided into a small
    number of runs. While n is large, we fold in bits from the lower order into r,
    and then add them back to n.
    """
    r = 0
    # Continue reducing n until it is less than 64, while accumulating the bits lost
    while n >= 64:
        r |= n & 1
        n //= 2
    return n + r

def binary_insertion_sort(arr, left, right):
    """
    Sort the subarray arr[left:right] using binary insertion sort.
    This is used to extend a run to a minimum length if it is too short.
    For each element, find the correct position within the sorted part (using binary search)
    and then shift elements to insert it.
    """
    for i in range(left + 1, right):
        key = arr[i]
        # Find insertion point via binary search
        lo = left
        hi = i
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] > key:
                hi = mid
            else:
                lo = mid + 1
        # Shift elements to the right to create space for key
        j = i
        while j > lo:
            arr[j] = arr[j - 1]
            j -= 1
        arr[lo] = key

def merge(arr, start, mid, end):
    """
    Merge two sorted subarrays: arr[start:mid] and arr[mid:end] into one sorted segment.
    This uses temporary arrays for both halves and then merges them back into arr.
    """
    left = arr[start:mid]
    right = arr[mid:end]
    i = j = 0
    k = start

    # Merge the two arrays until one is exhausted
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    # Copy any remaining elements from the left array
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    # Copy any remaining elements from the right array
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

def timsort(arr):
    """
    A simplified implementation of TimSort.
    
    Process:
    1. Calculate the minimum run size using calc_min_run.
    2. Traverse the array to identify naturally ordered runs. A run is a sequence that
       is either monotonically increasing or (if monotonically decreasing) reversed.
    3. If a run's length is less than the minimum run size, extend it using binary insertion sort.
    4. Record each run as a tuple (start_index, length).
    5. Merge the runs from the bottom of the stack until the entire array is sorted.
       (Note: This version uses a simplified merge strategy, merging the last two runs repeatedly.)
    """
    n = len(arr)
    if n <= 1:
        return arr

    min_run = calc_min_run(n)
    runs = []  # List to store runs as tuples: (start index, length)
    i = 0

    # Step 2: Identify natural runs in the array
    while i < n:
        run_start = i
        i += 1

        # Check if we have a descending or ascending run
        if i < n:
            if arr[i] < arr[i - 1]:
                # Descending run detected; move i until the run ends
                while i < n and arr[i] < arr[i - 1]:
                    i += 1
                # Reverse the descending run to make it ascending
                arr[run_start:i] = arr[run_start:i][::-1]
            else:
                # Ascending run detected; continue until the run ends
                while i < n and arr[i] >= arr[i - 1]:
                    i += 1

        run_end = i
        run_length = run_end - run_start

        # Step 3: If the run is shorter than min_run, extend it using binary insertion sort
        if run_length < min_run:
            # Determine the new end boundary, ensuring we don't exceed the array
            end = min(n, run_start + min_run)
            binary_insertion_sort(arr, run_start, end)
            run_end = end
            run_length = run_end - run_start
            i = run_end  # Move i to the end of this extended run
        
        # Record the current run
        runs.append((run_start, run_length))

    # Step 5: Merge the runs until the whole array is sorted
    # This simplified merge strategy always merges the last two runs in the stack.
    while len(runs) > 1:
        # Pop the last two runs
        run1_start, run1_length = runs.pop(-2)
        run2_start, run2_length = runs.pop(-1)
        # Merge these two runs
        merge(arr, run1_start, run1_start + run1_length, run1_start + run1_length + run2_length)
        # Push the merged run back onto the runs list
        merged_run = (run1_start, run1_length + run2_length)
        runs.append(merged_run)
    
    return arr

# Example usage:
if __name__ == "__main__":
    data = [5, 2, 9, 1, 5, 6, 7, 3, 2, 8]
    print("Original list:", data)
    sorted_data = timsort(data)
    print("Sorted list:", sorted_data)
