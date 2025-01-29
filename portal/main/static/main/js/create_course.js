document.addEventListener('DOMContentLoaded', function() {
    const testCheckbox = document.getElementById('has_test');
    const testForm = document.querySelector('.test-form');

    testCheckbox.addEventListener('change', function() {
        testForm.style.display = this.checked ? 'block' : 'none';
    });
});