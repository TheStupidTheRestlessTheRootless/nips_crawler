const puppeteer = require("puppeteer");
const _ = require("lodash");
const mockData = require('../mock.json');

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

(async () => {
    let browser = await puppeteer.launch({ headless: false });

    const doAdvancedQuery = async record => {
        const { name, organization: org } = record;
        const page = await browser.newPage();
        await page.setViewport({ width: 1200, height: 1500 });
        await page.goto(google_advanced_search);

        await page.waitForSelector(".otByu > .yIQOUb > .jYcx0e > .PLLUQc > #CwYCWc");
        await page.type(
            ".otByu > .yIQOUb > .jYcx0e > .PLLUQc > #CwYCWc",
            `"${name}" "${org}" "lab"`
        );

        await page.waitForSelector("form > .otByu > .yIQOUb > .jYcx0e > .jfk-button");
        await page.click("form > .otByu > .yIQOUb > .jYcx0e > .jfk-button");

        await page.waitForNavigation();
        await page.waitFor(1000);

        let res = await page.$(".g .rc .s");
        const val = await page.evaluate(el => el.innerText, res);
        const lab = parseLab(val);
        record.lab = lab;
        await page.close();
    };

    await Promise.all(
        mockData.map(item => {
            return doAdvancedQuery(item).catch((e) => { console.log(e); });
        })
    );

    console.log("lbao", mockData);
})();
