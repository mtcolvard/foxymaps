import React from 'react'

export default class CommuteVsExplore extends React.Component {
  constructor() {
    super()
    this.handleToggleClick = this.handleToggleClick.bind(this)
  }

  handleToggleClick() {
    this.props.onHandleToggleClick()
  }

  render() {
    const toggleExplore = this.props.toggleExplore
    return(
        <div className="commuteExploreField">
          <div className="level levelCommuteExplore is-mobile">
            <div className="level-item has-text-centered">
              <div>
                <p className="pCommuteExplore">Explore</p>
              </div>
            </div>
            <div className="level-item has-text-centered">
              <div>
                <input type="checkbox" id="toggle" className="checkbox" onClick={this.handleToggleClick} />
                <label htmlFor="toggle" className="switch"></label>
              </div>
            </div>
          </div>
        </div>
    )
  }
}
