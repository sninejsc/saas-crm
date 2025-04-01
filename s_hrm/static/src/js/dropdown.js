function toggleActiveOnParent(element) {
    const parentLi = element.closest('.custom-dropdown-class');
    if (parentLi) {
        parentLi.classList.toggle('active');
    }
}
