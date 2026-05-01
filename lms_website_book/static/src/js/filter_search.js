/** @odoo-module **/
const filterInputs = document.querySelectorAll(".filter-search");
function debounce(func, delay) {
  let debounceTimer;
  return function(...args) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => func.apply(this, args), delay);
  };
}
function filterDropdown(inputElement) {
  const filter = inputElement.value.toLowerCase();
  const dropdownItems = inputElement
    .closest(".filter-container")
    .querySelectorAll(".dropdown-item");
  dropdownItems.forEach(function(item) {
    const textContent = item.textContent.toLowerCase();
    item.classList.toggle("hidden", !textContent.includes(filter));
  });
}
filterInputs.forEach(function(inputElement) {
  const debouncedFilterDropdown = debounce(() => filterDropdown(inputElement), 300);
  inputElement.addEventListener("keyup", debouncedFilterDropdown);
});
