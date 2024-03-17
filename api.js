
const API_URL = 'https://d5dm5nc7bsaiu4esnh84.apigw.yandexcloud.net';

/**
 * @param {string} text
 * @param {string} clientId
 * @returns {Promise<{url: string}>}
 */
async function ttsApi(text, clientId) {
    const response = await fetch(`${API_URL}/tts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text,
            clientId,
        }),
    });
    const data = await response.json();
    return data;
}

/**
 * @param {string} text
 * @param {string} lang
 * @returns {Promise<string>}
 */
async function gpt(text, lang) {
    const response = await fetch(`${API_URL}/gpt`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text,
            lang
        }),
    });
    const data = await response.text();
    return data;
}

/**
 * 
 * @param {string} key
 * @returns {Promise<boolean>}
 */
async function checkStatus(key) {
    const response = await fetch(`${API_URL}/exs?file=${key}`);
    return response.status === 200;
}


async function generateVideo(clientId, url, avatarId) {
    const response = await fetch(`${API_URL}/avatar`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url,
            client_id: clientId,
            avatar_id: avatarId
        }),
    });
    const data = await response.json();
    return data;
}