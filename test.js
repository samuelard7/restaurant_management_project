function checking(nums){
    let i =0;
    for(let j=1;j<nums.length;j++){
        if(nums[i] !== nums[j]){
            i++;
            nums[i] = nums[j];
        }
    }
    return i + 1;
}
console.log([1,1,3,4]);