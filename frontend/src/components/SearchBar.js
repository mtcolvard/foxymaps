import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'


class SearchBar extends React.Component {
  constructor() {
    super()
    this.state = {
      publicButton: true,
      publicPrivateButton: false,
      privateButton: false
    }
    this.handleArrowLeftClick = this.handleArrowLeftClick.bind(this)
    this.handleDeleteFieldClick = this.handleDeleteFieldClick.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleButtonClick = this.handleButtonClick.bind(this)
  }

  handleArrowLeftClick() {
    this.props.onArrowLeft(this.props.name)
  }
  handleDeleteFieldClick() {
    this.props.onDeleteField(this.props.name)
  }
  handleChange(e) {
    this.props.onHandleChange(e)
  }
  handleSubmit(e) {
    e.preventDefault()
    this.props.onHandleSubmit(this.props.name)
  }

  handleButtonClick(buttonName) {
    this.props.handlePublicPrivateButtonClick(buttonName)
  }

  render() {
    const loadingSpinner =  this.props.loadingSpinner
    const {publicButton, publicPrivateButton, privateButton} = this.state
    return(
        <div className="field searchfield has-addons is-marginless" >
          <div className="control">
            <a className="button" onClick={this.handleArrowLeftClick}>
              <span className="icon iconbutton">
                <FontAwesomeIcon icon="arrow-left" />
              </span>
            </a>
          </div>
          <div className={ loadingSpinner ? "control is-loading is-expanded ": "control is-expanded"}>
            <form onSubmit={this.handleSubmit}>
              <input
                className="input is-focus"
                autoFocus
                autoComplete="off"
                type="text"
                placeholder={this.props.placeholder}
                onChange={this.handleChange}
                value={this.props.searchformData}
                name={this.props.name}
              />
            </form>
          </div>
          <div className="control">
            <a className="button" onClick={this.handleDeleteFieldClick}>
              <span className="icon iconbutton">
                <FontAwesomeIcon icon="times" />
              </span>
            </a>
          </div>
        </div>
    )
  }
}

export default SearchBar
