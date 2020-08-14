import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'


export default class SearchBarDirections extends React.Component {
  constructor() {
    super()
    this.handleArrowLeftClick = this.handleArrowLeftClick.bind(this)
    this.handleReverseOriginAndDestination = this.handleReverseOriginAndDestination.bind(this)
    this.triggerOriginSearchMenu = this.triggerOriginSearchMenu.bind(this)
    this.triggerDestinationSearchMenu = this.triggerDestinationSearchMenu.bind(this)
  }

  handleArrowLeftClick() {
    this.props.onArrowLeft()
  }

  handleReverseOriginAndDestination() {
    this.props.onReverseOriginAndDestination()
  }

  triggerOriginSearchMenu() {
    this.props.onTriggerOriginSearchMenu()
  }

  triggerDestinationSearchMenu() {
    this.props.onTriggerDestinationSearchMenu()
  }

  render() {
    const destination = this.props.destination
    const origin = this.props.origin
    const isMapboxSearching = this.props.isMapboxSearching
    return (
      <div>
      <div className="box funbox is-marginless">
        <div className="columns is-mobile is-vcentered">
          <div className="column funcolumn is-narrow">
            <a className="button iconbutton" onClick={this.handleArrowLeftClick}>
              <span className="icon">
                <FontAwesomeIcon icon="arrow-left" />
              </span>
            </a>
          </div>
          <div className="column centercolumn">
            <div className="field">
              <div className="control">
                <input
                  readOnly
                  className="input is-radiusless"
                  type="text"
                  placeholder="Choose starting point"
                  value={origin}
                  onClick={this.triggerOriginSearchMenu}
                />
              </div>
              <div className="control">
                <input
                  readOnly
                  className="input is-radiusless"
                  type="text"
                  placeholder="Choose destination"
                  value={destination}
                  onClick={this.triggerDestinationSearchMenu}
                />
              </div>
            </div>
          </div>
          <div className="column funcolumn is-narrow">
            <a className="button iconbutton" onClick={this.handleReverseOriginAndDestination}>
              <span className="icon">
                <FontAwesomeIcon icon="arrows-alt-v" />
              </span>
            </a>
          </div>
        </div>
      </div>
      {isMapboxSearching ? <progress className="progress is-small is-info" max="100">20%</progress>: ''}
      </div>
    )
  }
}
