
// Wait until page fully loads
document.addEventListener('DOMContentLoaded', function () {

    // Get member select field
    const membersSelect = $('#members');

    // Check Select2 exists
    if (!membersSelect.length || !$.fn.select2) {
        console.warn('Select2 or #members not found');
        return;
    }

    // Initialize Select2
    membersSelect.select2({

        theme: 'bootstrap-5',

        placeholder: 'Search member',

        allowClear: true,

        width: '100%'

    });

    // Auto focus search box when dropdown opens
    membersSelect.on('select2:open', function () {

        const searchField =
            document.querySelector('.select2-search__field');

        if (searchField) {
            searchField.focus();
        }

    });

});