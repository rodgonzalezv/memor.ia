document.addEventListener('DOMContentLoaded', function() {
    const radius = 240; // how big of the radius
    const autoRotate = true; // auto rotate or not
    const rotateSpeed = -60; // unit: seconds/360 degrees
    const imgWidth = 120; // width of images (unit: px)
    const imgHeight = 170; // height of images (unit: px)

    setTimeout(init, 100);

    const odrag = document.getElementById("drag-container");
    const ospin = document.getElementById("spin-container");
    const aImg = ospin.getElementsByTagName("img");
    const aVid = ospin.getElementsByTagName("video");
    const aEle = ospin.querySelectorAll(".item"); // combine 2 arrays

    ospin.style.width = imgWidth + "px";
    ospin.style.height = imgHeight + "px";

    const ground = document.getElementById("ground");
    ground.style.width = radius * 3 + "px";
    ground.style.height = radius * 3 + "px";

    function init(delayTime) {
        const items = document.querySelectorAll('#spin-container .item');
        items.forEach((item, i) => {
            item.style.transform = `rotateY(${i * (360 / items.length)}deg) translateZ(${radius}px)`;
            item.style.transition = "transform 1s";
            item.style.transitionDelay = `${delayTime || (items.length - i) / 4}s`;
        });
    }

    function applyTransform(obj) {
        tY = Math.min(Math.max(tY, 0), 180);
        obj.style.transform = `rotateX(${-tY}deg) rotateY(${tX}deg)`;
    }

    function playSpin(yes) {
        ospin.style.animationPlayState = yes ? "running" : "paused";
    }

    let sX, sY, nX, nY, desX = 0, desY = 0, tX = 0, tY = 10;

    if (autoRotate) {
        const animationName = rotateSpeed > 0 ? "spin" : "spinRevert";
        ospin.style.animation = `${animationName} ${Math.abs(rotateSpeed)}s infinite linear`;
    }

    document.addEventListener('pointerdown', function(e) {
        clearInterval(odrag.timer);
        sX = e.clientX;
        sY = e.clientY;

        document.addEventListener('pointermove', onPointerMove);
        document.addEventListener('pointerup', onPointerUp);
    });

    function onPointerMove(e) {
        nX = e.clientX;
        nY = e.clientY;
        desX = nX - sX;
        desY = nY - sY;
        tX += desX * 0.1;
        tY += desY * 0.1;
        applyTransform(odrag);
        sX = nX;
        sY = nY;
    }

    function onPointerUp() {
        odrag.timer = setInterval(function() {
            desX *= 0.95;
            desY *= 0.95;
            tX += desX * 0.1;
            tY += desY * 0.1;
            applyTransform(odrag);
            playSpin(false);
            if (Math.abs(desX) < 0.5 && Math.abs(desY) < 0.5) {
                clearInterval(odrag.timer);
                playSpin(true);
            }
        }, 17);
        document.removeEventListener('pointermove', onPointerMove);
        document.removeEventListener('pointerup', onPointerUp);
    }

    document.addEventListener('wheel', function(e) {
        e = e || window.event;
        const d = e.wheelDelta / 20 || -e.detail;
        radius += d;
        init(1);
    });

    const lightbox = document.getElementById('lightbox');
    const img = lightbox.querySelector('img');
    const caption = lightbox.querySelector('.overlay-caption');
    const commentSection = lightbox.querySelector('#comment-section');
    const commentList = commentSection.querySelector('#comment-list');
    const commentForm = commentSection.querySelector('#comment-form');
    let currentFamiliarId = null;

    const spinContainer = document.getElementById('spin-container');
    spinContainer.addEventListener('click', function(event) {
        if (event.target.closest('.item a')) {
            event.preventDefault();
            const anchor = event.target.closest('.item a');
            img.src = anchor.href;
            caption.textContent = anchor.querySelector('p') ? anchor.querySelector('p').textContent : "Image";
            lightbox.classList.add('active');

            // Set current familiar ID
            currentFamiliarId = anchor.closest('.item').dataset.familiarId;

            // Fetch and display comments
            fetchComments(anchor.href);
        }
    });

    lightbox.addEventListener('click', function(event) {
        if (event.target !== img && !commentSection.contains(event.target) && !commentForm.contains(event.target)) {
            lightbox.classList.remove('active');
            setTimeout(() => {
                img.src = ''; // Clear the image source after the transition
            }, 500);
        }
    });

    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const commentText = commentForm.querySelector('textarea').value;
        if (commentText.trim() === '') return;

        // Post the comment
        postComment(commentText, img.src, currentFamiliarId);
        commentForm.reset();
    });

    const crudButton = document.getElementById('crud-button');
    const crudOverlay = document.getElementById('crud-overlay');
    const crudCloseButton = document.getElementById('crud-close-button');
    const addForm = document.getElementById('add-familiar-form');
    const removeList = document.getElementById('remove-familiar-list');
    const editList = document.getElementById('edit-familiar-list');

    crudButton.addEventListener('click', function() {
        crudOverlay.style.display = 'flex';
        hideAllForms();
    });

    crudCloseButton.addEventListener('click', function() {
        crudOverlay.style.display = 'none';
    });

    crudOverlay.addEventListener('click', function(event) {
        if (event.target === crudOverlay) {
            crudOverlay.style.display = 'none';
        }
    });

    document.getElementById('crud-add-button').addEventListener('click', function() {
        hideAllForms();
        addForm.style.display = 'block';
    });

    document.getElementById('crud-remove-button').addEventListener('click', function() {
        hideAllForms();
        removeList.style.display = 'block';
        populateRemoveList();
    });

    document.getElementById('crud-edit-button').addEventListener('click', function() {
        hideAllForms();
        editList.style.display = 'block';
        populateEditList();
    });

    function hideAllForms() {
        document.querySelectorAll('.crud-form').forEach(form => {
            form.style.display = 'none';
        });
    }

    document.getElementById('add-image-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
    
        const imageFile = document.getElementById('new-image').files[0];
        const reader = new FileReader();
        reader.onload = function(e) {
            const newImgUrl = e.target.result;
            const familiarId = document.querySelector('.item').dataset.familiarId;

            const newItem = document.createElement('div');
            newItem.className = 'item';
            newItem.dataset.familiarId = familiarId;
            newItem.innerHTML = `
                <a href="${newImgUrl}" target="_blank">
                    <img src="${newImgUrl}" alt="Familiar Image"/>
                    <p>New Familiar</p>
                </a>
            `;
            document.getElementById('spin-container').appendChild(newItem);
    
            updateCarousel(); // Update the carousel
            addEventListenersToNewItem(newItem); // Add event listener to the new item

            // Upload the image to the server
            const formData = new FormData();
            formData.append('image', imageFile);
            formData.append('familiar_id', familiarId);

            fetch('/carousel/upload_image/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Image uploaded:', data);
                newItem.querySelector('a').href = data.url;
                newItem.querySelector('img').src = data.url;
            })
            .catch(error => {
                console.error('Error uploading image:', error);
            });

            crudOverlay.style.display = 'none'; // Close the overlay
        };
        reader.readAsDataURL(imageFile); // This converts the image file to a data URL
    });
    
    function updateCarousel() {
        init(1); // Reinitialize the carousel with a delay time of 1
    }

    function populateRemoveList() {
        const removeList = document.getElementById('remove-list');
        removeList.innerHTML = '';
        const items = document.querySelectorAll('#spin-container .item');
        items.forEach((item, index) => {
            const listItem = document.createElement('li');
            const itemText = item.querySelector('p') ? item.querySelector('p').textContent : `Image ${index + 1}`;
            listItem.textContent = itemText;
            listItem.addEventListener('click', function() {
                item.remove(); // Remove the clicked item
                updateCarousel(); // Update the carousel
                hideOverlay();
            });
            removeList.appendChild(listItem);
        });
    }

    function populateEditList() {
        const editList = document.getElementById('edit-list');
        editList.innerHTML = '';
        const items = document.querySelectorAll('#spin-container .item');
        items.forEach((item, index) => {
            const listItem = document.createElement('li');
            const itemText = item.querySelector('p') ? item.querySelector('p').textContent : `Image ${index + 1}`;
            listItem.textContent = itemText;
            listItem.addEventListener('click', function() {
                const newText = prompt('Edit the name of the Familiar:', itemText);
                if (newText) {
                    if (item.querySelector('p')) {
                        item.querySelector('p').textContent = newText;
                    } else {
                        const p = document.createElement('p');
                        p.textContent = newText;
                        item.appendChild(p);
                    }
                    updateCarousel(); // Update the carousel
                    hideOverlay();
                }
            });
            editList.appendChild(listItem);
        });
    }

    function addEventListenersToNewItem(item) {
        item.querySelector('a').addEventListener('click', function(event) {
            event.preventDefault();
            img.src = this.href;
            caption.textContent = this.querySelector('p') ? this.querySelector('p').textContent : "Image";
            lightbox.classList.add('active');
    
            // Set current familiar ID
            currentFamiliarId = item.dataset.familiarId;
    
            // Fetch comments for the selected image
            fetchComments(this.href);
        });
    }

    function fetchComments(imageUrl) {
        console.log('Fetching comments for:', imageUrl);
        fetch(`/carousel/comments/fetch/?image_url=${encodeURIComponent(imageUrl)}&familiar_id=${encodeURIComponent(currentFamiliarId)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Comments fetched:', data);
                commentList.innerHTML = '';
                data.forEach(comment => {
                    const commentItem = document.createElement('li');
                    commentItem.textContent = `${comment.username} (${comment.created_at}): ${comment.text}`;
                    commentList.appendChild(commentItem);
                });
            })
            .catch(error => {
                console.error('Error fetching comments:', error);
            });
    }

    function postComment(text, imageUrl, familiarId) {
        console.log('Posting comment to:', imageUrl);
        fetch('/carousel/comments/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ text, image_url: imageUrl, familiar_id: familiarId })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Comment posted:', data);
            const commentItem = document.createElement('li');
            commentItem.textContent = `${data.username} (${data.created_at}): ${data.text}`;
            commentList.appendChild(commentItem);
        })
        .catch(error => {
            console.error('Error posting comment:', error);
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
