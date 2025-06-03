"use strict";

(function() {

  // MODULE GLOBAL VARIABLES, CONSTANTS, AND HELPER FUNCTIONS CAN BE PLACED HERE

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
    testButton.addEventListener("click", test_hash_table);
  }

  function hash_function(key) {
    let hash = 0;

    const prime_numbers = [23, 29, 31, 37, 41, 43, 47, 53]

    for (let i = 0; i < key.length; i++) {
      hash += prime_numbers[i] * prime_numbers[i] * (key[i].charCodeAt(0));
    }

    return hash;
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
      button.style.backgroundColor = `rgb(${colorValue}, ${colorValue}, 255)`; // Blueish gradient
    }
  }


  function calculate_hash(testSize, inputRange, bucketSize) {
    const dict = new Map();
    for (let i = 0; i < testSize; i++) {
      const rand = Math.floor(Math.random() * inputRange); // random int [0, 99999999]
      const hash = hash_function(rand.toString());

      const index = hash % bucketSize;
      const current = dict.get(index) || 0;
      dict.set(index, current + 1);
    }

    show_color(dict);
  }


  function test_hash_table() {
    const bucketSize = id('bucket-input').value;
    const testSize = id('test-input').value;
    const inputRange = id('range-input').value;

    show_grids(bucketSize);

    calculate_hash(testSize, inputRange, bucketSize);

  }

  function show_grids(bucketSize) {
    const grids = qs(".grids");
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

  /**
   * Returns a new element with the given tag name.
   * @param {string} tagName - HTML tag name for new DOM element.
   * @returns {object} New DOM object for given HTML tag.
   */
  function gen(tagName) {
    return document.createElement(tagName);
  }

})();