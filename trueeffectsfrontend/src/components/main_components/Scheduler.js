import React, {useState} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar'
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {connect} from 'react-redux';
import 'moment/locale/pl';
import "../../new_sass/scheduler.scss"
import {getSingleTraining, getTrainings} from "../../redux/actions/trainingActions";
import {useHistory} from "react-router-dom";
import {BoxLoading} from "react-loadingg";
import {handleMoveToModifyTraining} from "../helpers/history_helpers";
import {t} from "i18next";

require('moment/locale/pl.js')

const Scheduler = (props) => {
    const history = useHistory()
    const localizer = momentLocalizer(moment)
    let events = []
    if (props.trainings !== undefined) {
        props.trainings.map(el => {
            events.push({
                'id': el.id,
                'title': el.name,
                'date': el.date,
                'start': moment(Date.parse(el.date)).toDate(),
                'end': moment(Date.parse(el.date)).toDate()
            })
            return events
        })
    }
    const handleSelect = async (e) => {
        await handleMoveToModifyTraining(history, e.id)
    }
    return props.trainingsLoaded ? (
        <div className="scheduler">
            <div className="scheduler__title">
                {t("Training Calendar")}
            </div>
            <div className="schedule">
                <Calendar
                    culture={t("language_code")}
                    views={['month']}
                    selectable={true}
                    events={events}
                    onSelectEvent={handleSelect}
                    localizer={localizer}
                    style={{height: 900, width: '100%'}}
                />
            </div>
        </div>
    ) : props.trainingsLoading && (
        <div className="box-loading">
            <BoxLoading/>
        </div>
    )
}
const mapStateToProps = (state) => {
    return {
        trainings: state.training.trainings.data,
        trainingsLoading: state.training.trainingsLoading,
        trainingsLoaded: state.training.trainingsLoaded,
        trainingForModal: state.training.trainingForModal
    }
}
export default connect(mapStateToProps, {getTrainings, getSingleTraining})(Scheduler);
