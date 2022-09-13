var socket;
var seqList;
var seqFrames;
var time;

function powerOff() {
    // switch to on button display
    $('#connected').css('display','none');
    $('#not-connected').css('display','block');
	$('#wmsg-load-seq').text("");
 
    	closeSocket();
}

function powerOn() {
    $('#wmsg-load-seq').text("Loading sequences (may take a while)...");

    openSocket();
}

function reset() {
	dofs = ['tower_1', 'tower_2', 'tower_3', 'base', 'ears'];
	for (let dof=0; dof < dofs.length; dof++) {
		if (dofs[dof] === 'base') {
			$('#'+dofs[dof]+'-input').val(0);
			updateSliderVal(0,dofs[dof]);
		} else if (dofs[dof] === 'ears') {
			$('#'+dofs[dof]+'-input').val(-100);
			updateSliderVal(-100,dofs[dof]);
		} else{
			$('#'+dofs[dof]+'-input').val(100);
			updateSliderVal(100,dofs[dof]);
		};
	}
}

function recordSequence() {
	if ($('#record-seq-name').val() === ""){
		// no name given by user
		$('#wmsg').text("[!] error: enter a valid sequence name before recording");
	} else if (seqList.includes($('#record-seq-name').val())){
		// name already exists
		$('#wmsg').text("[!] error: sequence name already exists");
	} else {
		// switch to 'stop' recording button
		$('#not-recording').css('display','none');
		$('#recording').css('display','block');
		$('#wmsg').text("prepare to record");

		// request the motor positions
		setTimeout(function(){
		$('#wmsg').text("begin recording");
		const frameTimeInt = 100; //milliseconds 
		recordInt = setInterval(function() {
			dofs = ["tower_1", "tower_2", "tower_3", "base", "ears"];
			motorPos = [];
			for (let dof=0; dof < dofs.length; dof++) {
				motorPos.push({"dof": dofs[dof], "pos": $('#' + dofs[dof] + '-input').val()/50 + 3});
			}

			// create a frame_list object
			var time = parseInt($('#timer').text());
			var frameBlock = {"positions": motorPos, "millis": time};

			// update timer
			$('#timer').text(time + frameTimeInt);
			socket.emit('record_sequence',frameBlock);
			}, frameTimeInt);
			},2500);
	}
}

function stopSequence() {
	$('#wmsg').text("");

	// switch to 'record' recording button
	$('#not-recording').css('display','block');
	$('#recording').css('display','none');

	// send new sequence name and clear input text
	seqList.push($('#record-seq-name').val());
	input = {'sequence_name':$('#record-seq-name').val()}
	socket.emit('stop_sequence',input);
	$('#record-seq-name').val("");
	clearInterval(recordInt);
	$('#timer').text(0);
}

function loadSequence(is_time_input) {
	seqName = $('#play-seq-name').val();

	if (seqName === ""){
		// no name given by user
		$('#wmsg').text("[!] error: input sequence name to load");

	} else if(!seqList.includes(seqName)){
		$('#wmsg').text("[!] error: sequence name does not exist");
	} else{
		// name exists in seq_list...
		$('#wmsg').text("");
		$('#slide-seq-name').text(seqName);

		// retrieve the json file of the sequence
		input = {'sequence_name':seqName};
		socket.emit('retrieve_seq_file',input);
		socket.on('get_seq_file', function(data) {
			console.log("Retrieving .json file....")
			seqFrames = data["frame_list"]

			// store the millis/time frame of requested sequence
			time = [];
			for (let frame=0; frame < seqFrames.length; frame++) {
				time.push(seqFrames[frame]["millis"]);
			}
			time.reverse();

			if (is_time_input) {
				// change the max value of playback slider by time
				maxRangeTime = seqFrames[seqFrames.length-1]["millis"]
				$('#playback-slider').slider("option","max",maxRangeTime);
				$('#playback-slider').slider("option","step",10);
			} else {
				// change the max value of playback slider by frames
				maxRangeFrames = seqFrames.length-1;
				$('#playback-slider').slider("option","max",maxRangeFrames);
				$('#playback-slider').slider("option","step",1);
			}
			frameData = {'sequence_name':'temp_playback', 'frame_list':seqFrames};
			socket.emit('save_playback',frameData);
			$('#playback').css('display','block');
		});
	}
}

function updatePlayback(input,is_time_input,is_edit) {
	if (is_time_input) {
		// update the frame timer
		function findFrame(value){
		if (value === input){return true}
		}
		frameIdx = time.findIndex(findFrame);
		$('#slide-frame').text(frameIdx);

		// update the millis timer
		$('#slide-millis').text(input);

		function findClosestMilli(value){
			//find the closest time without going over
			timeDif = input - value;
			if (timeDif >= 0){return true}
		}

		frameIdx = time.length - (time.findIndex(findClosestMilli)+1);
		frameBlock = seqFrames[frameIdx]["positions"];
	} else {
		// update the frame timer
		$('#slide-frame').text(input);
		// update the millis timer
		$('#slide-millis').text(seqFrames[input]["millis"]);

		frameIdx = input;
		frameBlock = seqFrames[frameIdx]["positions"];
	}

	// update the motor sliders
	dofs = ['tower_1', 'tower_2', 'tower_3', 'base', 'ears'];
	num_dofs_in_block = frameBlock.length;
	if (is_edit) {
		for (let dof=0; dof<dofs.length; dof++){
			if (dof <= num_dofs_in_block){
				motorVal = $('#' + dofs[dof] + '-input').val()/50 + 3;
				frameBlock[dof]["dof"] = dofs[dof];
				frameBlock[dof]["pos"] = motorVal;
			} else {
				frameBlock.push({"dof": dofs[dof], "pos": motorVal});
			};
		};
		seqFrames[frameIdx]["positions"] = frameBlock;

		$('#wmsg-playback').text("successfully save frame " + input.toString());
		setTimeout(function(){
			$('#wmsg-playback').text("");},2000); //wait 2 seconds
		frameData = {'sequence_name':'temp_playback','frame_list':seqFrames};
		socket.emit('save_playback',frameData);
	} else {
		var data = {};
		for (let motor=0; motor<frameBlock.length; motor++){
			data[frameBlock[motor]["dof"]] = 50 * (frameBlock[motor]["pos"] - 3); //deg
		};
		socket.emit('move_robot',data);

		for (let dof=0; dof < dofs.length; dof++) {
			dofStr = dofs[dof];
			motorValDeg = data[dofStr]
			motorValRad = motorValDeg/50 + 3;

			// update sliders
			$('#slide-' + dofStr + '-deg').text(motorValDeg);
			$('#slide-' + dofStr + '-rad').text(motorValRad);
			$('#' + dofStr + '-input').val(motorValDeg);
		};
	};
}

function savePlayback() {
	seqName = $('#playback-seq-name').val();
	if (seqName === "") {
		$('#wmsg-playback').text("[!] error: enter a valid sequence name before saving playback");
	} else if (seqList.includes(seqName)) {
		$('#wmsg-playback').text("[!] error: sequence name already exists");
	} else {
		$('#wmsg-playback').text("");
		frameData = {'sequence_name': seqName, 'frame_list':seqFrames};
		socket.emit('save_playback',frameData);

		// add new sequence name and reset text box
		seqList.push(seqName);
		$('#playback-seq-name').val("");
	}
}

function playSequence(input) {
    	frameData = {'sequence_name':input};
	socket.emit('play_sequence',frameData);
    	$('#play-seq-name').val("");
}

function updateMotorPos(motor) {
	socket.emit('update_motor',motor,$('#' + motor + '-input').val());
}

function updateSliderVal(slideVal, motor) {
	$('#slide-' + motor + '-deg').text(slideVal);
	$('#slide-' + motor + '-rad').text(slideVal / 50 + 3);
}

function openSocket() {
    // initialize socket
    socket = io.connect('http://' + document.domain + ':' + location.port, {'forceNew':true});
    // event listener for when the connection to the server is established
    socket.on('connect', function() {
        console.log('Connected socket')
	});

	socket.on('get_seq_list', function(data) {
		// obtain an array containing strings of blossom's sequences
		data = data.replace(/\s+/g, '');
		data = data.replace(/['"]+/g, '');
		data = data.slice(1,data.length-1);
		seqList = data.split(',');

		// switch to controller display
		$('#not-connected').css('display','none');
		$('#connected').css('display','block');
		$('#recording').css('display','none');
		$('#playback').css('display','none');
		$('#wmsg-loading-seq').text("");

		console.log('Received sequence names list')
	});
}

function closeSocket() {
    // send disconnect msg to server
    socket.disconnect();
    console.log('Disconnect socket');
}
