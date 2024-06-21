function bubbleSort(arr) {
  let n = arr.length;
  for (let i = 0; i < n - 1; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
      }
    }
  }
  return arr;
}

function quickSort(arr, left = 0, right = arr.length - 1) {
  if (left < right) {
    const pivotIndex = partition(arr, left, right);
    quickSort(arr, left, pivotIndex - 1);
    quickSort(arr, pivotIndex + 1, right);
  }
  return arr;
}

function partition(arr, left, right) {
  const pivot = arr[right];
  let i = left - 1;
  for (let j = left; j < right; j++) {
    if (arr[j] < pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }
  [arr[i + 1], arr[right]] = [arr[right], arr[i + 1]];
  return i + 1;
}

let startTime = new Date();

const array1 = [64, 34, 25, 12, 22, 11, 72];
console.log("Sorted array:", bubbleSort(array1));
let endTime = new Date();
let elapsed = endTime - startTime;
console.log(`bubble 실행 시간: ${elapsed}ms`);

startTime = new Date();
const array = [64, 34, 25, 12, 22, 11, 72];
console.log("Sorted array:", quickSort(array));
endTime = new Date();
elapsed = endTime - startTime;
console.log(`quick 실행 시간: ${elapsed}ms`);
