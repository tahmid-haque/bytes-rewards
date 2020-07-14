const rest_img = document.querySelector('#restaurant-image'),
    url_input = document.querySelector('input[type="url"]'),
    location_inputs = document.querySelectorAll('input[readonly]'),
    postal_input = document.querySelector(
        'input[name="location[postal_code]"]'
    ),
    long_inputs = document.querySelectorAll('textarea'),
    postal_code = /[A-Z]\d[A-Z]\d[A-Z]\d/;

/*
    Update the province/city inputs by adjusting readonly.
*/
function updateLocationInputs(city, province) {
    location_inputs[0].readOnly = false;
    location_inputs[1].readOnly = false;
    location_inputs[0].value = city;
    location_inputs[1].value = province;
    location_inputs[0].readOnly = true;
    location_inputs[1].readOnly = true;
}

/*
    Update the province/city inputs using the given postal code.
*/
function updateLocation() {
    const value = postal_input.value.toUpperCase();
    postal_input.value = value;
    if (value.match(postal_code) !== null) {
        postal_input.setCustomValidity('Please wait for city/province lookup.');
        fetch('https://geocoder.ca/' + value + '?json=1')
            .then((res) => res.json())
            .then((data) => {
                console.log(data.standard.city);
                if (
                    !('error' in data) &&
                    typeof data.standard.city === 'string' &&
                    typeof data.standard.prov === 'string'
                ) {
                    updateLocationInputs(
                        data.standard.city,
                        data.standard.prov
                    );
                    postal_input.setCustomValidity('');
                } else
                    postal_input.setCustomValidity(
                        'Please provide a valid Postal Code.'
                    );
            });
    } else {
        updateLocationInputs('', '');
        postal_input.setCustomValidity('Please provide a valid Postal Code.');
    }
}

/*
    Show the restaurant image with an animation.
*/
function showImage() {
    rest_img.classList.remove('scale-out');
    rest_img.classList.remove('hidden');
    rest_img.classList.add('scale-in');
    url_input.setCustomValidity('');
}

/*
    Hide the restaurant image with an animation.
*/
function hideImage() {
    rest_img.classList.remove('scale-in');
    rest_img.classList.add('scale-out');
    setTimeout(() => {
        rest_img.classList.add('hidden');
    }, 500);
    url_input.setCustomValidity('Please provide a loadable image.');
}

/*
    Scale textarea height depending on content.
*/
function setInputHeight(input) {
    input.style.height = input.scrollHeight + 'px';
}

/*
    Update the image using the image input. Hide/show appropriately.
*/
function updateImage() {
    rest_img.src = url_input.value;
    setTimeout(() => {
        if (rest_img.complete && rest_img.height > 0) {
            showImage();
        } else hideImage();
    }, 1000);
}

/*
    Initialize the location, textarea and image elements.
*/
window.onload = () => {
    updateLocation();
    long_inputs.forEach((e) => {
        setInputHeight(e);
    });
    updateImage();
};

long_inputs.forEach((e) => {
    // Adjust text area height depending on content
    e.oninput = () => setInputHeight(e);
});
postal_input.oninput = updateLocation; // Update location inputs on data change
rest_img.onerror = hideImage; // Hide image when there's an error
url_input.onchange = updateImage; // Update image on image url change
