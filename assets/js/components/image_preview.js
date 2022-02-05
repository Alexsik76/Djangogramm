export default {
  name: 'ImagePreview',
  delimiters: ['[[', ']]'],
  props:
    ['name', 'value'],

  data() {
    console.log(this.value, this.name)
    return {
      url: this.value || "https://via.placeholder.com/150",
      file_name: this.name,
    }
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
      this.file_name = file.name
    }
  },
  template:`
  <div class="column is-three-fifths">
            <div id="with_filename" class="file has-name is-boxed">
                <label class="file-label">
                    <input id="imgInput" class="file-input" type="file" name="image" @change="onFileChange"
                           accept="image/*">
                    <span class="file-cta">
                        <span class="file-icon"><i class="fas fa-upload"></i></span>
                        <span class="file-label">Choose a file...</span>
                    </span>
                    <span class="file-name">[[file_name]]</span>
                </label>
            </div>
        </div>
    <div class="box" style="padding: 0.5rem">
        <figure class="image" style="width: 128px">
          <img id="imgPrev" :src="url" alt="Loaded image"/>
        </figure>
    </div>
  `

}
