document.addEventListener('DOMContentLoaded', function () {

    const searchInput = document.getElementById('project-search');
    const projectRows = document.querySelectorAll('.project-row');

    if (!searchInput || projectRows.length === 0) {
        return;
    }

    searchInput.addEventListener('input', function () {

        const searchText = searchInput.value.toLowerCase();

        projectRows.forEach(function (row) {

            const rowText = row.textContent.toLowerCase();

            if (rowText.includes(searchText)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }

        });

    });

});