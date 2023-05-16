import {Link} from 'react-router-dom';
import {useState} from 'react';
import { Helmet } from "react-helmet";

import MapMenu from '../mapMenu/MapMenu';
import Header from '../header/Header';
import QuestionForm from '../questionForm/QuestionForm';

import '../app/App.scss';

const MapPage = () => {
    const [questionVisib, setQuestionVisib] = useState(false)
    const [helpVisib, setHelpVisib] = useState(false)

    const onQuestionVisib = () => {
        setQuestionVisib(!questionVisib);
    }

    const onHelpVisib = () => {
        setHelpVisib(!helpVisib)
    }

    return (
        <div className="App">

            <Helmet>
                <meta
                    name="description"
                    content="Карта для обнаружения маршрутов героев книг"
                />
                <title>Book Trip Map</title>
            </Helmet>

            <Header onQuestionVisib={onQuestionVisib} onHelpVisib={onHelpVisib}/>

            <div className="main">
                <MapMenu/>

                <QuestionForm onQuestionVisib={onQuestionVisib} questionVisib={questionVisib}/>


                <div className={`back-info modal-win ${helpVisib ? '' : 'hide'}`}>
                    <div className="back-info__container modal-win__cont">
                        <div className="modal-win__title yellow-font">Справочная информация</div>
                        <div onClick={onHelpVisib} className="close"></div>
                        <div className="back-info__text">
                            <div className="back-info__text__scroll">
                                <p>
                                1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ac purus placerat, 
                                volutpat felis vel, suscipit ex. Sed in egestas elit. Vestibulum ante ipsum primis in 
                                faucibus orci luctus et ultrices posuere cubilia curae; Aenean tristique quam eu tortor 
                                dapibus, sit amet suscipit metus commodo. Donec efficitur odio ligula, sit amet 
                                scelerisque neque pellentesque rutrum 
                                </p>
                                <p>
                                2. Ut sed magna dictum, dignissim velit sit amet, viverra ex. Proin imperdiet convallis 
                                vulputate. Sed dictum mi in vestibulum placerat. Donec dui purus, vestibulum in condimentum 
                                et, pharetra eget arcu. Integer aliquet neque ornare purus lacinia, eu cursus lectus hendrerit. 
                                In volutpat venenatis tincidunt. Phasellus sit amet est sagittis, malesuada diam at, vestibulum tortor.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

        </div>
    );
}

export default MapPage;