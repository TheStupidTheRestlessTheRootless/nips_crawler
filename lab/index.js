const puppeteer = require("puppeteer");
const _ = require("lodash");
const fs = require("fs");
// const data = require("../mock.json");
const data = require("../output.json");

const google_advanced_search = "https://www.google.com/advanced_search";

const key_word = "lab";
const stop_words = ["the", "at", "in"];
const punctuation = [".", ",", "!", ":"];

const parseLab = txt => {
    words = txt.toLowerCase().split(" ");
    let index = words.indexOf(key_word);
    if (index === -1) {
        return "";
    }

    let lab = [];
    for (; index >= 0; index--) {
        let word = words[index];
        last_char = word.substring(word.length - 1);
        if (stop_words.indexOf(words[index]) !== -1 || punctuation.indexOf(last_char) !== -1) {
            break;
        }

        lab.unshift(words[index]);
    }

    return lab.join(" ");
};

const timeout = ms => {
    return new Promise(resolve => setTimeout(resolve, ms));
};

let browser;

const doAdvancedQuery = async record => {
    const { name, organization: org } = record;
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 1500 });
    await page.goto(google_advanced_search);

    await page.waitForSelector(".otByu > .yIQOUb > .jYcx0e > .PLLUQc > #CwYCWc");
    await page.type(".otByu > .yIQOUb > .jYcx0e > .PLLUQc > #CwYCWc", `"${name}" "${org}" "lab"`);

    await page.waitForSelector("form > .otByu > .yIQOUb > .jYcx0e > .jfk-button");
    await page.click("form > .otByu > .yIQOUb > .jYcx0e > .jfk-button");

    await page.waitForNavigation();

    await page.waitForSelector(".g .rc .s", { timeout: 1000 });
    let res = await page.$(".g .rc .s");
    const val = await page.evaluate(el => el.innerText, res);
    const lab = parseLab(val);
    record.lab = lab;
    fs.writeFileSync(`./temp/${record.id}`, JSON.stringify(record));
    await page.close();
};

(async () => {
    if (!fs.existsSync("./temp")) {
        fs.mkdirSync("./temp");
    }
    browser = await puppeteer.launch({ headless: false });

    for (let item of data) {
        if (fs.existsSync(`./temp/${item.id}`)) {
            continue;
        }

        await doAdvancedQuery(item).catch(e => {
            console.log(e);
        });
        await timeout(5000);
    }

    await browser.close();
})();
