// Connect to the SocketIO server
var socket = io();

// Get the existing <div> from the webpage
const container = document.getElementById('sensor-data-container');

/* Creates the sensor group containers with the sensor card elements in them 
*  for displaying in a grid format on the webpage
*/
function create_topic_elements(topic)
{
    // Splits the topic (sensor/<type>/id) into 3 different variables
    const parts      = topic.split('/');
    const sensorType = parts[1].toUpperCase();
    const sensorID   = parts[2].split('-').pop();

    const element_id = topic.replace('/', '_'); 
    const group_id   = `group_${sensorID}`;
    
    let groupContainer = document.getElementById(group_id);

    // If the container doesn't already exist then create a new grop container
    if (!groupContainer)
    {
        console.log(`[DOM] - Creating new group container for ID: ${sensorID}`);

        groupContainer = document.createElement('div');
        groupContainer.className = 'sensor-group';
        groupContainer.id = group_id;

        container.appendChild(groupContainer);
    }

    var target_element = document.getElementById(element_id);

    // If the sensor card doesn't already exist this creates it 
    if(!target_element)
    {
        console.log(`[DOM] - Creating new element for topic: ${topic}`);

        const elementCard = document.createElement('div');
        elementCard.className = 'sensor-card';

        const topicLabel = document.createElement('p');
        topicLabel.innerText = sensorType + ' ' + sensorID + ':';

        const valueContainer = document.createElement('span');
        valueContainer.id = element_id;
        valueContainer.innerText = "Initializing...";
        valueContainer.className = 'sensor-value';

        elementCard.appendChild(topicLabel);
        elementCard.appendChild(valueContainer);

        groupContainer.appendChild(elementCard);

        target_element = valueContainer;
    }
    return target_element;
}   

// 2. Define the listener function
socket.on('new_sensor_data', function(data) {
    var topic = data.topic;
    var value = data.value;
    
    // Extract the simple ID from the topic (e.g., 'sensors/moisture' -> 'sensors_moisture')
    const target_element = create_topic_elements(topic);
    console.log(target_element);

    // 3. Update the HTML element if it exists
    if (target_element) {
        const nice_value = value.split(" ")
        target_element.innerText = nice_value[1];

        target_element.style.opacity = 0;
        setTimeout(() => {
            target_element.style.opacity = 1;
        }, 50);
    }
    console.log(`Update: ${topic} = ${value}`);
});

socket.on('connect', function() {
    console.log('Successfully connected to Flask WebSocket.');
});

socket.on('disconnect', function() {
    console.log('Disconnected from Flask WebSocket.');
});