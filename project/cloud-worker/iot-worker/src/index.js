/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

async function getCreateRecord(db, selectSQL, insertSQL, params, idName)
{
	let stmt = db.prepare(selectSQL).bind(...params);
	let results = await stmt.first();

	console.log(results);	

	if (results)
	{
		return results[idName];
	}

	stmt = db.prepare(insertSQL).bind(...params);
	let insertResults = await stmt.run();

	if (insertResults.success && insertResults.meta.last_row_id)
	{
		return insertResults.meta.last_row_id;
	}

	console.log("Attempting SELECT: ", selectSQL, params);
	stmt = db.prepare(selectSQL).bind(...params);
	results = await stmt.first();

	if (results)
	{
		return results[idName];
	}

	throw new Error(`Failed to create or retrieve lined record ID!`);
}

export default {
	async fetch(request, env, ctx) {
		if (request.method !== "POST")
		{
			return new Response("Send as a POST with JSON body", {status: 400});
		}

		if (!env.DB)
		{
			return new Response('Database binding (env.DB) not found!', {status: 500});
		}

		const { DB } = env;
		let data;

		try 
		{
			data = await request.json();
		}
		catch(e)
		{
			return new Response('Invalid JSON payload!', { status: 400 });
		}

		const readBatch = [];

		try
		{
			for (const [greenhouseName, sensors] of Object.entries(data))
			{
				const ghSelectSQL = 'SELECT greenhouse_id FROM greenhouses WHERE name = ?';
				const ghInsertSQL = 'INSERT INTO greenhouses (name) VALUES(?)';

				const greenhouseID = await getCreateRecord(
					DB,
					ghSelectSQL,
					ghInsertSQL,
					[greenhouseName],
					'greenhouse_id'
				);

				for (const [deviceName, readings] of Object.entries(sensors))
				{
					const sensorSelectSQL = 'SELECT sensor_id FROM sensors WHERE greenhouse_id = ? AND device_name = ?';
					const sensorInsertSQL = 'INSERT INTO sensors (greenhouse_id, device_name) VALUES(?, ?)';
					const sensorID = await getCreateRecord(
						DB,
						sensorSelectSQL,
						sensorInsertSQL,
						[greenhouseID, deviceName],
						'sensor_id'
					);

					const timestamp = readings.timestamp;

					const readingInsertSQL = 'INSERT INTO sensor_readings (sensor_id, type, value) VALUES (?, ?, ?)';

					for (const [type, value] of Object.entries(readings))
					{
						const stmt = DB.prepare(readingInsertSQL).bind(
							sensorID,
							type,
							value
						);

						readBatch.push(stmt);
					}
				}
			}
			if (readBatch.length > 0)
			{
				const results = await DB.batch(readBatch);
				const totalInserts = results.length;

				return new Response(`Successfully processed and inserted ${totalInserts} reading records!`, { status: 201 });
			}
			else
			{
				return new Response('No reading data found in the payload!', { status: 200 });
			}
		}
		catch (e)
		{
			console.error(e);
			return new Response(`Database error: ${e.message}`, { status: 500 });
		}

		/*
		try
		{
			const data = await request.json();


			
			Object.keys(data).forEach(greenhouseID => {
				const greenhouseDevices = data[greenhouseID];
				console.log(`\n--- Processing ${greenhouseID} ---`);

				Object.keys(greenhouseDevices).forEach(rpiID => {
					const deviceData = greenhouseDevices[rpiID];

					console.log(`	Device: ${rpiID}`);

					Object.keys(deviceData).forEach(dataKey => {
						const dataValue = deviceData[dataKey];

						console.log(`		- ${dataKey}; ${dataValue}`);
					});
				});
			});

			return new Response("Data recieved!");
		}
		catch (err)
		{
			return new ReportingObserver(JSON.stringify({error: "Invalid JSON body"}), {
				status: 400,
				headers: {"Content-Type": "application/json"}
			});
		}
		*/
	},
};
