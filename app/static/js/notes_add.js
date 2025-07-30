document.addEventListener('DOMContentLoaded', function () {
  // Sync contenteditable div to hidden textarea before form submit
  document.getElementById('noteForm').addEventListener('submit', function () {
    const editorContent = document.getElementById('notes-editor').innerHTML.trim();
    document.getElementById('notes-hidden').value = editorContent;
  });

  // Show image preview
  const imageInput = document.getElementById('image');
  const preview = document.getElementById('image-preview');

  imageInput.addEventListener('change', function (e) {
    const file = e.target.files[0];

    if (file) {
      const reader = new FileReader();
      reader.onload = function (event) {
        preview.src = event.target.result;
        preview.style.display = 'block';

        // Create remove checkbox if not already present
        if (!document.getElementById('remove-preview-image')) {
          const checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.id = 'remove-preview-image';
          checkbox.className = 'form-check-input me-1';

          // Hidden input to send form value to backend
          const hiddenInput = document.createElement('input');
          hiddenInput.type = 'hidden';
          hiddenInput.id = 'remove-image-flag';
          hiddenInput.name = 'remove_image';
          hiddenInput.value = '0';

          const label = document.createElement('label');
          label.htmlFor = 'remove-preview-image';
          label.className = 'form-check-label';
          label.innerText = 'Remove selected image';

          const wrapper = document.createElement('div');
          wrapper.className = 'form-check mt-2';
          wrapper.id = 'preview-remove-wrapper';

          wrapper.appendChild(checkbox);
          wrapper.appendChild(label);
          wrapper.appendChild(hiddenInput);
          preview.insertAdjacentElement('afterend', wrapper);

          checkbox.addEventListener('change', function () {
            preview.style.display = this.checked ? 'none' : 'block';
            hiddenInput.value = this.checked ? '1' : '0';
          });
        } else {
          // Reset checkbox if already exists
          const checkbox = document.getElementById('remove-preview-image');
          const hiddenInput = document.getElementById('remove-image-flag');
          checkbox.checked = false;
          hiddenInput.value = '0';
          preview.style.display = 'block';
        }
      };
      reader.readAsDataURL(file);
    } else {
      // No file selected
      preview.src = "";
      preview.style.display = 'none';

      // Remove checkbox if exists
      const wrapper = document.getElementById('preview-remove-wrapper');
      if (wrapper) wrapper.remove();
    }
  });

  // Force plain text paste
  const editor = document.getElementById('notes-editor');
  editor.addEventListener('paste', function (e) {
    e.preventDefault();
    const text = (e.clipboardData || window.clipboardData).getData('text/plain');
    document.execCommand('insertText', false, text);
  });
});

