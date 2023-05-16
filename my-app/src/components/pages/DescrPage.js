import './Descr.scss';
import {Link} from 'react-router-dom';
import { Helmet } from "react-helmet";

import logo from '../../resources/img/logo.png';
import map1 from '../../resources/descrPage/map_1.png';
import map2 from '../../resources/descrPage/map_2.png';
import man from '../../resources/descrPage/participants/man.png';
import women from '../../resources/descrPage/participants/women.png';

const DescrPage = () => {
    return (
        <div className="descrPage">

            <Helmet>
                <meta
                    name="description"
                    content="Краткое представление картографического веб-приложения с анализом текста книг"
                />
                <title>Book Trip</title>
            </Helmet>

            <section id="up" className="promo">
                <div className="container">
                    <header className="promo__header">
                        <div className="header__log">
                            <img src={logo} alt="logo"/>
                        </div>
                        <ul className="promo__menu">
                            <li className="promo__menu__item">
                                <a href="#tag-descr" className="promo__menu__link yellow-font">Описание</a>
                            </li>
                            <li className="promo__menu__item">
                                <a href="#tag-patric" className="promo__menu__link yellow-font">Участники</a>
                            </li>
                        </ul>
                    </header>
                    <div className="promo__wrapper">
                        <div className="promo__start">
                            <h1 className="promo__start__title yellow-font">Вместе с героями</h1>
                            <p className="promo__start__subtitle">Загрузи любимое литературное произведение  и проследи за
                                передвижениями персонажей на реальной карте мира</p>
                        </div>
                        <Link to='/map'>
                            <button className="promo__button transition-btn">На карту</button>
                        </Link>
                    </div>
                </div>
            </section>

            <section className="description">
                <a name="tag-descr"></a>
                <div className="container">
                    <div className="description__wrapper">
                        <img src={map1} alt="Картинка для описания" className="description__image"/>
                        <div className="description__block">
                            <h2 className="description__header yellow-font">Описание</h2>
                            <p className="description__text text-view">Вот вам яркий пример современных тенденций — убеждённость 
                                некоторых оппонентов не даёт нам иного выбора, кроме определения позиций, занимаемых 
                                участниками в отношении поставленных задач. В частности, семантический разбор внешних 
                                противодействий предоставляет широкие возможности для поэтапного и последовательного развития общества. 
                                Банальные, но неопровержимые выводы, а также акционеры крупнейших компаний освещают чрезвычайно интересные 
                                особенности картины в целом, однако конкретные выводы, разумеется, смешаны с не уникальными данными до степени 
                                совершенной неузнаваемости, из-за чего 
                                возрастает их статус бесполезности.</p>
                        </div>
                    </div>
                </div>
            </section>

            <section className="principles">
                <div className="container">
                    <div className="principles__wrapper">
                        <div className="principles__content">
                            <h2 className="principles__content__header yellow-font">Принципы работы</h2>
                            <p className="principles__content__descr text-view">В целом, конечно, глубокий уровень погружения выявляет срочную 
                                потребность распределения внутренних резервов и ресурсов. Каждый из нас понимает очевидную вещь: 
                                консультация с широким активом предполагает независимые способы реализации экономической целесообразности 
                                принимаемых решений.</p>
                        </div>
                        <img src={map2} alt="Картинка под принципы" className="principles__image"/>
                    </div>
                </div>
            </section>

            <section className="participants">
                <a name="tag-patric"></a>
                <div className="container">
                    <h2 className="participants__title yellow-font">Участники</h2>
                    <div className="participants__list">
                        <div className="participants__item">
                            <img src={women} alt="Разработчик" className="participants__item__image"/>
                            <div className="participants__item__data">
                                <div className="participants__item__fullname">Иванова Илона Ивановна</div>
                                <div className="participants__item__specialization">разработчик</div>
                            </div>
                        </div>
                        <div className="participants__item">
                            <img src={man} alt="Руководитель" className="participants__item__image"/>
                            <div className="participants__item__data">
                                <div className="participants__item__fullname">Иванов Иван Иванович</div>
                                <div className="participants__item__specialization">руководитель</div>
                            </div>
                        </div>
                        <div className="participants__item">
                            <img src={women} alt="Участник 3" className="participants__item__image"/>
                            <div className="participants__item__data">
                                <div className="participants__item__fullname">Иванова Илона Ивановна</div>
                                <div className="participants__item__specialization">разработчик</div>
                            </div>
                        </div>
                        <div className="participants__item">
                            <img src={man} alt="Участник 4" className="participants__item__image"/>
                            <div className="participants__item__data">
                                <div className="participants__item__fullname">Иванов Иван Иванович</div>
                                <div className="participants__item__specialization">руководитель</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section className="transition">
                <div className="container">
                    <Link to='/map'>
                        <button className="transition-btn">На карту</button>
                    </Link>
                </div>
            </section>

            <footer className="footer">
                <div className="container">
                    <div className="footer__wrapper">
                        <div className="header__logo">
                            <img src={logo} alt="logo"/>
                        </div>
                        <div className="footer__years">@2023</div>
                    </div>
                </div>
            </footer>
        </div>
    )
}

export default DescrPage;