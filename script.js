const allCards = [
    "10 Дунариев", "10 Жезлов", "10 Кубков", "10 Мечей",
    "2 Дунариев", "2 Жезлов", "2 Кубков", "2 Мечей",
    "3 Дунариев", "3 Жезлов", "3 Кубков", "3 Мечей",
    "4 Дунариев", "4 Жезлов", "4 Кубков", "4 Мечей",
    "5 Дунариев", "5 Жезлов", "5 Кубков", "5 Мечей",
    "6 Дунариев", "6 Жезлов", "6 Кубков", "6 Мечей",
    "7 Дунариев", "7 Жезлов", "7 Кубков", "7 Мечей",
    "8 Дунариев", "8 Жезлов", "8 Кубков", "8 Мечей",
    "9 Дунариев", "9 Жезлов", "9 Кубков", "9 Мечей",
    "Башня", "Влюбленные", "Дьявол", "Жрец", "Жрица",
    "Звезда", "Император", "Императрица", "Колесница",
    "Колесо Фортуны", "Королева Дунариев", "Королева Жезлов",
    "Королева Кубков", "Королева Мечей", "Король Дунариев",
    "Король Жезлов", "Король Кубков", "Король Мечей", "Луна",
    "Маг", "Мир", "Отшельник", "Повешенный", "Паж Дунариев",
    "Паж Жезлов", "Паж Кубков", "Паж Мечей", "Рыцарь Дунариев",
    "Рыцарь Жезлов", "Рыцарь Кубков", "Рыцарь Мечей", "Сила",
    "Смерть", "Солнце", "Справедливость", "Суд", "Туз Дунариев",
    "Туз Жезлов", "Туз Кубков", "Туз Мечей", "Умеренность", "Шут"
];

const cardImages = {
    "10 Дунариев": "assets/10_дунариев.png",
    "10 Жезлов": "assets/10_жезлов.png",
    "10 Кубков": "assets/10_кубков.png",
    "10 Мечей": "assets/10_мечей.png",
    "2 Дунариев": "assets/2_дунариев.png",
    "2 Жезлов": "assets/2_жезлов.png",
    "2 Кубков": "assets/2_кубков.png",
    "2 Мечей": "assets/2_мечей.png",
    "3 Дунариев": "assets/3_дунариев.png",
    "3 Жезлов": "assets/3_жезлов.png",
    "3 Кубков": "assets/3_кубков.png",
    "3 Мечей": "assets/3_мечей.png",
    "4 Дунариев": "assets/4_дунариев.png",
    "4 Жезлов": "assets/4_жезлов.png",
    "4 Кубков": "assets/4_кубков.png",
    "4 Мечей": "assets/4_мечей.png",
    "5 Дунариев": "assets/5_дунариев.png",
    "5 Жезлов": "assets/5_жезлов.png",
    "5 Кубков": "assets/5_кубков.png",
    "5 Мечей": "assets/5_мечей.png",
    "6 Дунариев": "assets/6_дунариев.png",
    "6 Жезлов": "assets/6_жезлов.png",
    "6 Кубков": "assets/6_кубков.png",
    "6 Мечей": "assets/6_мечей.png",
    "7 Дунариев": "assets/7_дунариев.png",
    "7 Жезлов": "assets/7_жезлов.png",
    "7 Кубков": "assets/7_кубков.png",
    "7 Мечей": "assets/7_мечей.png",
    "8 Дунариев": "assets/8_дунариев.png",
    "8 Жезлов": "assets/8_жезлов.png",
    "8 Кубков": "assets/8_кубков.png",
    "8 Мечей": "assets/8_мечей.png",
    "9 Дунариев": "assets/9_дунариев.png",
    "9 Жезлов": "assets/9_жезлов.png",
    "9 Кубков": "assets/9_кубков.png",
    "9 Мечей": "assets/9_мечей.png",
    "Башня": "assets/башня.png",
    "Влюбленные": "assets/влюбленные.png",
    "Дьявол": "assets/дьявол.png",
    "Жрец": "assets/жрец.png",
    "Жрица": "assets/жрица.png",
    "Звезда": "assets/звезда.png",
    "Император": "assets/император.png",
    "Императрица": "assets/императрица.png",
    "Колесница": "assets/колесница.png",
    "Колесо Фортуны": "assets/колесо_фортуны.png",
    "Королева Дунариев": "assets/королева_дунариев.png",
    "Королева Жезлов": "assets/королева_жезлов.png",
    "Королева Кубков": "assets/королева_кубков.png",
    "Королева Мечей": "assets/королева_мечей.png",
    "Король Дунариев": "assets/король_дунариев.png",
    "Король Жезлов": "assets/король_жезлов.png",
    "Король Кубков": "assets/король_кубков.png",
    "Король Мечей": "assets/король_мечей.png",
    "Луна": "assets/луна.png",
    "Маг": "assets/маг.png",
    "Мир": "assets/мир.png",
    "Отшельник": "assets/отшельник.png",
    "Повешенный": "assets/повешенный.png",
    "Паж Дунариев": "assets/паж_дунариев.png",
    "Паж Жезлов": "assets/паж_жезлов.png",
    "Паж Кубков": "assets/паж_кубков.png",
    "Паж Мечей": "assets/паж_мечей.png",
    "Рыцарь Дунариев": "assets/рыцарь_дунариев.png",
    "Рыцарь Жезлов": "assets/рыцарь_жезлов.png",
    "Рыцарь Кубков": "assets/рыцарь_кубков.png",
    "Рыцарь Мечей": "assets/рыцарь_мечей.png",
    "Сила": "assets/сила.png",
    "Смерть": "assets/смерть.png",
    "Солнце": "assets/солнце.png",
    "Справедливость": "assets/справедливость.png",
    "Суд": "assets/суд.png",
    "Туз Дунариев": "assets/туз_дунариев.png",
    "Туз Жезлов": "assets/туз_жезлов.png",
    "Туз Кубков": "assets/туз_кубков.png",
    "Туз Мечей": "assets/туз_мечей.png",
    "Умеренность": "assets/умеренность.png",
    "Шут": "assets/шут.png"
};


const selectedCards = [];
const randomCards = allCards.sort(() => 0.5 - Math.random()).slice(0, 10);

function renderCards() {
    const container = document.getElementById("cards-container");
    container.innerHTML = "";
    randomCards.forEach((card, index) => {
        const cardElement = document.createElement("div");
        cardElement.className = "card";
        cardElement.innerHTML = `
            <div class="card-inner">
                <div class="card-back"></div>
                <div class="card-front">
                    <img src="${cardImages[card]}" alt="${card}" />
                    <p>${card}</p>
                </div>
            </div>
        `;
        cardElement.addEventListener("click", () => toggleCard(cardElement, index));
        container.appendChild(cardElement);
    });
}

function toggleCard(cardElement, index) {
    if (selectedCards.length < 3 && !selectedCards.includes(index)) {
        selectedCards.push(index);
        cardElement.classList.add("flipped");
    }

    if (selectedCards.length === 3) {
        submitCards();
    }
}

function submitCards() {
    const selectedCardNames = selectedCards.map(index => randomCards[index]);
    const data = {
        question: question,
        cards: selectedCardNames.join(", ")
    };
    Telegram.WebApp.sendData(JSON.stringify(data)); // Отправляем вопрос и карты
    Telegram.WebApp.close(); // Закрываем мини-приложение
}

renderCards();