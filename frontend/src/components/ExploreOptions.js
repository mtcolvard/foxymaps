import React from 'react'

export default class ExploreOptions extends React.Component {
  constructor() {
    super()
    this.handlePublicButtonClick = this.handlePublicButtonClick.bind(this)
    this.handlePublicPrivateButtonClick = this.handlePublicPrivateButtonClick.bind(this)
    this.handlePrivateButtonClick = this.handlePrivateButtonClick.bind(this)
  }

  handlePublicButtonClick() {
    this.props.onHandlePublicPrivateButtonClick('publicButton')
  }
  handlePublicPrivateButtonClick() {
    this.props.onHandlePublicPrivateButtonClick('publicPrivateButton')
  }
  handlePrivateButtonClick() {
    this.props.onHandlePublicPrivateButtonClick('privateButton')
  }
  render() {
    const publicButton = this.props.publicButton
    const publicPrivateButton = this.props.publicPrivateButton
    const privateButton = this.props.privateButton

    return(
        <div className="field searchfield has-addons">
          <p className="control">
            <button className={publicButton ? "button is-info is-selected" : "button"} onClick={this.handlePublicButtonClick}>
              <span>Public</span>
            </button>
          </p>
          <p className="control">
            <button className={publicPrivateButton ? "button is-info is-selected" : "button"} onClick={this.handlePublicPrivateButtonClick}>
              <span>Public & Private</span>
            </button>
          </p>
          <p className="control">
            <button className={privateButton ? "button is-info is-selected" : "button"} onClick={this.handlePrivateButtonClick}>
              <span>Private</span>
            </button>
          </p>
        </div>
    )
  }
}
