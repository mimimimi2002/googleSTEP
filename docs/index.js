"use strict";

(function() {

  // MODULE GLOBAL VARIABLES, CONSTANTS, AND HELPER FUNCTIONS CAN BE PLACED HERE
  let bucketSize;
  let testSize;
  let inputRange;
  /**
   * Add a function that will be called when the window is loaded.
   */
  window.addEventListener("load", init);

  /**
   * Initializes the event listeners for the task and section buttons.
   * The "Add Task" button is linked to the addTask function, and
   * the "Add Section" button is linked to the addSection function.
   * This sets the buttons for creating new tasks and sections
   * on the webpage.
   */
  function init() {
    let testButton = id("test-button");
    testButton.addEventListener("click", click_test_button);
    let modes = qsa(".circle");
    for (let i = 0; i < modes.length; i++) {
      modes[i].addEventListener("click", chooseMode);
    }
  }

  function chooseMode(e) {
    let mode = e.target.id;

    // deactivate all the modes
    let modes = qsa(".circle");
    for (let i = 0; i < modes.length; i++) {
      modes[i].classList.remove("active");
    }

    if (mode === "canvas-mode") {
      let canvasMode = qs("#canvas-mode");
      canvasMode.classList.add("active");
      let numberMode = qs("#number-mode");
      numberMode.classList.remove("active");
      let canvas = qs("#canvas");
      canvas.classList.remove("hidden");
      let numbers = qs(".numbers");
      numbers.classList.add("hidden");
    }
    if (mode === "number-mode") {
      let numberMode = qs("#number-mode");
      numberMode.classList.add("active");
      let canvasMode = qs("#canvas-mode");
      canvasMode.classList.remove("active");
      let canvas = qs("#canvas");
      canvas.classList.add("hidden");
      let numbers = qs(".numbers");
      numbers.classList.remove("hidden");
    }
  }

  function show_color(dict) {
    // First, find the max count for normalization
    console.log(dict)
    let maxCount = 0;
    for (const count of dict.values()) {
      if (count > maxCount) maxCount = count;
    }

    // Color each button based on its count
    for (const [index, count] of dict.entries()) {
      const button = id(index);
      if (!button) continue;

      // Normalize count to [0, 1]
      const brightness = count / maxCount;

      // Convert brightness to a color if the index has many elements, the color will be closer to blue.
      const colorValue = Math.floor(255 * (1 - brightness));
      button.style.backgroundColor = `rgb(255, ${colorValue}, ${colorValue})`; // Blueish gradient
    }
  }

  function show_results(dict) {
    const results = qs(".results");
    results.classList.remove("hidden");
    // Calculate variance and standard deviation
    let counts = [];
    let total = 0;

    // Gather counts of all buckets (fill 0 if missing)
    for (let i = 0; i < bucketSize; i++) {
      const count = dict.get(i) || 0;
      counts.push(count);
      total += count;
    }

    const mean = total / bucketSize;

    // Variance = average squared difference from the mean
    const variance = counts.reduce((acc, c) => acc + (c - mean) ** 2, 0) / bucketSize;

    // Standard deviation = sqrt(variance)
    const stddev = Math.sqrt(variance);

    id("mean").textContent = mean.toFixed(2);
    id("variance").textContent = variance.toFixed(2);
    id("standard-deviation").textContent = stddev.toFixed(2);
    id("max-size").textContent = Math.max(...counts)
    id("min-size").textContent = Math.min(...counts)
    console.log(`Mean bucket size: ${mean.toFixed(2)}`);
    console.log(`Variance: ${variance.toFixed(2)}`);
    console.log(`Standard deviation: ${stddev.toFixed(2)}`);
    console.log(`Max bucket size: ${Math.max(...counts)}`);
    console.log(`Min bucket size: ${Math.min(...counts)}`);
  }


  function calculate_hash(testSize, inputRange, bucketSize, new_hash_function) {
    const dict = new Map();
    const rands = getRandomUniqueNumbers(testSize, 0, inputRange);
    for (let i = 0; i < testSize; i++) {
      const rand = rands[i];
      const hash = new_hash_function(rand.toString());

      const index = hash % bucketSize;
      const current = dict.get(index) || 0;
      dict.set(index, current + 1);
    }

    return dict;
  }

  function getRandomUniqueNumbers(count, min, max) {
    const numbers = [];
    const range = [];

    // Create an array with numbers from min to max
    for (let i = min; i <= max; i++) {
      range.push(i);
    }

    // Shuffle the array
    for (let i = range.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [range[i], range[j]] = [range[j], range[i]];
    }

    // Take the first 'count' numbers
    return range.slice(0, count);
  }




  function click_test_button() {
    bucketSize = id('bucket-input').value;
    testSize = id('test-input').value;
    inputRange = id('range-input').value;

    let hashFunction = id("hash-function").value;
    let new_hash_function = evaluate_hash_function(hashFunction);
    console.log(new_hash_function("hello"));

    const dict = calculate_hash(testSize, inputRange, bucketSize, new_hash_function);

    // draw campus
    draw_campus(dict, bucketSize);

    // draw grid numbers
    show_grids_with_numbers(bucketSize);
    show_color(dict);

    show_modes();

    show_results(dict);
  }

  function evaluate_hash_function(inputBody) {
    try {
      const wrappedCode = `
      function hash_function(key) {
        ${inputBody}
      }
    `;
      const wrapper = new Function(wrappedCode + "; return hash_function;");
      const fn = wrapper();

      if (typeof fn === "function") {
        return fn;
      } else {
        alert("No valid function found.");
      }

    } catch (e) {
      alert("Error in function: " + e.message);
      console.error(e);
    }
  }

  function show_modes() {
    let modes = qs(".modes");
    modes.classList.remove("hidden");

    let numberMode = qs("#number-mode");
    numberMode.classList.add("active");
    let canvasMode = qs("#canvas-mode");
    canvasMode.classList.remove("active");
    let canvas = qs("#canvas");
    canvas.classList.add("hidden");
    let numbers = qs(".numbers");
    numbers.classList.remove("hidden");
  }

  function show_grids_with_numbers(bucketSize) {
    const grids = qs(".numbers");
    grids.innerHTML = ""

    for (let i = 0; i < bucketSize; i++) {
      const numberButton = gen("button");
      numberButton.textContent = i;

      // Add classes and styles
      numberButton.className = 'w-full h-full';
      numberButton.className = "number-button"
      numberButton.style.width = '50px';
      numberButton.style.height = '50px';
      numberButton.id = i
      grids.appendChild(numberButton);
    }
  }

  function draw_campus(dict, bucketSize) {
    const width = Math.floor(Math.sqrt(bucketSize));
    const height = Math.floor(Math.sqrt(bucketSize));

    const pixelSize = window.innerWidth / width;

    const canvas = document.getElementById('canvas');
    canvas.width = window.innerWidth;
    canvas.height = height * pixelSize;
    const ctx = canvas.getContext('2d');

    let maxCount = 0;
    for (const count of dict.values()) {
      if (count > maxCount) maxCount = count;
    }

    for (const [index, count] of dict.entries()) {
      const x = index % width;
      const y = Math.floor(index / width);

      const brightness = count / maxCount;
      const colorValue = Math.floor(255 * (1 - brightness));

      ctx.fillStyle = `rgb(255, ${colorValue}, ${colorValue})`;
      ctx.fillRect(x * pixelSize, y * pixelSize, pixelSize, pixelSize);
    }
  }



  /** ------------------------------ Helper Functions  ------------------------------ */
  /**
   * Note: You may use these in your code, but remember that your code should not have
   * unused functions. Remove this comment in your own code.
   */

  /**
   * Returns the element that has the ID attribute with the specified value.
   * @param {string} idName - element ID
   * @returns {object} DOM object associated with id.
   */
  function id(idName) {
    return document.getElementById(idName);
  }

  /**
   * Returns the first element that matches the given CSS selector.
   * @param {string} selector - CSS query selector.
   * @returns {object} The first DOM object matching the query.
   */
  function qs(selector) {
    return document.querySelector(selector);
  }

  function qsa(selector) {
    return document.querySelectorAll(selector);
  }

  /**
   * Returns a new element with the given tag name.
   * @param {string} tagName - HTML tag name for new DOM element.
   * @returns {object} New DOM object for given HTML tag.
   */
  function gen(tagName) {
    return document.createElement(tagName);
  }

})();