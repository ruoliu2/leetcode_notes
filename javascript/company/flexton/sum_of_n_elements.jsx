// Given an array of integers, return an list of integers which contains [1st integer, Sum of next 2
// integers (2nd, 3rd), Sum of next 3 integers (4th, 5th, 6th)] and so on so on.
// Input :: [1,6,8,5,9,4,7,2] Output :: [1,14,18,9]
// in the result 1st Value - 1 2nd Value - 6 + 8 -> 14 3rd Value - 5 + 9 + 4 -> 18 4th Value - 7 + 2 ->
// Sum of next Four elements but four elements are not present in the array so will sum up the
// remaining values -> 9
// Your algorithms should work for assuming there can be n elements in the array
function sumArray(arr) {
  let result = [];
  let i = 0;
  let step = 1;

  while (i < arr.length) {
    // Sum the next step elements from the array
    let sum = 0;
    for (let j = 0; j < step && i < arr.length; j++, i++) {
      sum += arr[i];
    }
    result.push(sum);
    // increment the step
    step++;
  }

  return result;
}

// Example usage:
const inputArray = [1, 6, 8, 5, 9, 4, 7, 2];
const output = sumArray(inputArray);
console.log(output); // Output: [1, 14, 18, 9]
