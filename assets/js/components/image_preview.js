export default {
  name: 'ImagePreview',
  props:
    ['label', 'name', 'value'],

  data() {
    return {
      url: "https://via.placeholder.com/150",
      file_name: null
    }
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
      console.log(file)
      this.file_name = file.name
    }
  },
  template:`
  <div class="column is-two-fifths">
            <div id="with_filename" class="file has-name">
                <label class="file-label">
                    <input id="imgInput" class="file-input" type="file" name="{{ name }}" @change="onFileChange"
                           accept="image/*">
                    <span class="file-cta">
                        <span class="file-icon"><i class="fas fa-upload"></i></span>
                        <span class="file-label">{{ label }}</span>
                    </span>
                    <span class="file-name">{{file_name}}</span>
                </label>
            </div>
        </div>
    <div class="box" style="padding: 0.5rem">
        <figure class="image" style="width: 128px">
            
          <img id="imgPrev" v-if="url" :src="url" alt="Loaded image"/>

        </figure>
    </div>
  `

}
