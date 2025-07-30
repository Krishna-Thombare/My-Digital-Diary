document.addEventListener('DOMContentLoaded', function () {
  // Sync editable div to hidden textarea on submit
  document.getElementById('editNoteForm').addEventListener('submit', function () {
    const content = document.getElementById('notes-editor').innerHTML.trim();
    document.getElementById('notes-hidden').value = content;
  });

  const imageInput = document.getElementById('image');
  const preview = document.getElementById('image-preview');
  const oldImageContainer = document.getElementById('existing-image');

  imageInput.addEventListener('change', function (e) {
    const file = e.target.files[0];

    if (file) {
      const label = document.querySelector('label[for="image"]');
      if (label) {
        label.textContent = '📷 Change Image';
      }

      const reader = new FileReader();
      reader.onload = function (event) {
        preview.src = event.target.result;
        preview.style.display = 'block';

        if (oldImageContainer) {
          oldImageContainer.style.display = 'none';
        }

        if (!document.getElementById('remove-preview-image')) {
          const checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.id = 'remove-preview-image';
          checkbox.name = 'remove_image';
          checkbox.className = 'form-check-input me-1';

          const label = document.createElement('label');
          label.htmlFor = 'remove-preview-image';
          label.className = 'form-check-label';
          label.innerText = 'Remove selected image';

          const wrapper = document.createElement('div');
          wrapper.className = 'form-check mt-2';
          wrapper.id = 'preview-remove-wrapper';

          wrapper.appendChild(checkbox);
          wrapper.appendChild(label);

          preview.insertAdjacentElement('afterend', wrapper);

          checkbox.addEventListener('change', function () {
            preview.style.display = checkbox.checked ? 'none' : 'block';
          });
        } else {
          document.getElementById('remove-preview-image').checked = false;
          preview.style.display = 'block';
        }
      };
      reader.readAsDataURL(file);
    } else {
      preview.src = "";
      preview.style.display = 'none';

      if (oldImageContainer) {
        oldImageContainer.style.display = 'block';
      }

      const wrapper = document.getElementById('preview-remove-wrapper');
      if (wrapper) wrapper.remove();
    }
  });

  document.getElementById('remove-image')?.addEventListener('change', function () {
    const existingImage = document.querySelector('#existing-image img');
    if (this.checked && existingImage) {
      existingImage.style.display = 'none';
    } else if (existingImage) {
      existingImage.style.display = 'block';
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
